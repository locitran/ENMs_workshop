"""

ChEMBL web services API live documentation Explorer
https://www.ebi.ac.uk/chembl/api/data/docs
"""


import time

from .utils.tools import openURL, ALLdictElement, dictElement
from xml.etree.cElementTree import XML
from .utils.logger import LOGGER

class ChemblRecord(object):
    """Wrapper for CHEMBL data with methods for accessing fields and parsing related PDB entries."""
    
    def __init__(self, data):
        self._rawdata = data
        self._parse()
            
    def __repr__(self):
        return '<ChemblRecord: %s>' % self.getTitle()

    def __str__(self):
        return self.getTitle()

    def getChemblID(self, index=0):
        return self.getEntry('target_chembl_id', index)

    def getType(self, index=0):
        return self.getEntry('target_type', index)
    
    def getOrganism(self, index=0):
        return self.getEntry('organism', index)
    
    def getSpeciesGroup(self, index=0):
        return self.getEntry('species_group_flag', index)

    def getName(self, index=0):
        return self.getEntry('pref_name', index)

    def getTaxonomy(self, index=0):
        return self.getEntry('tax_id', index)

    def getXML(self):
        return f'https://www.ebi.ac.uk/chembl/api/data/target/{0}?format=xml'.format(self.getAccession())

    def setData(self, value):
        self._rawdata = value
        self._parse()

    def getData(self):
        return self._rawdata
    
    def getTitle(self):
        chemblid = self.getChemblID()
        name = self.getName()
        return f'{chemblid} ({name})'

    def getEntry(self, item, index=0):
        key = f'{item}{index:4d}'
        if key in self._rawdata:
            return self._rawdata[key]
        else:
            raise KeyError(f'{item} does not exist in the record')

    def getCrossReferences(self):
        return self._cross_references

    def getTargetComponents(self):
        return self._target_components

    def _children(self, d, prefix):
        return [v for k, v in d.items() if isinstance(v, dict) and k.strip().startswith(prefix)]

    def _str(self, d, field):
        for k, v in d.items():
            if k.strip().startswith(field) and isinstance(v, str):
                return v
        return None

    def _parseCrossReferences(self):
        """
        Parse *target-level* cross references from self._rawdata.

        Handles both of these shapes (numbered keys allowed):
        A) cross_references -> target -> xref_id / xref_name / xref_src / xref_url
        B) target_xrefs     -> target_xref -> xref_src_db / xref_id / xref_url

        Populates: self._cross_references = [
        {"source": ..., "xref_id": ..., "xref_name": ..., "url": ...}, ...
        ]
        """
        xrefs = []
        # --- A) cross_references -> target -> xref_*
        # Example provided:
        # {'cross_references   0': {'target   0': {'xref_id   0': 'CPX-1795',
        #   'xref_name   0': 'Integrin alphav-beta3 complex', 'xref_src   0': 'ComplexPortal'}}}
        for cr in self._children(self._rawdata, 'cross_references'):
            for tgt in self._children(cr, 'target'):
                entry = {
                    "source":    self._str(tgt, 'xref_src') or self._str(tgt, 'xref_src_db'),
                    "xref_id":   self._str(tgt, 'xref_id'),
                    "xref_name": self._str(tgt, 'xref_name'),
                    "url":       self._str(tgt, 'xref_url'),
                }
                # keep entries that have at least an id + source or a name
                if entry.get("xref_id") or entry.get("xref_name"):
                    xrefs.append(entry)

        # --- B) legacy/alternate: target_xrefs -> target_xref -> xref_*
        for tx in self._children(self._rawdata, 'target_xrefs'):
            for one in self._children(tx, 'target_xref'):
                entry = {
                    "source":    self._str(one, 'xref_src_db') or self._str(one, 'xref_src'),
                    "xref_id":   self._str(one, 'xref_id'),
                    "xref_name": self._str(one, 'xref_name'),
                    "url":       self._str(one, 'xref_url'),
                }
                if entry.get("xref_id") or entry.get("xref_name"):
                    xrefs.append(entry)

        # De-duplicate (source, id, name, url)
        seen = set()
        out = []
        for e in xrefs:
            key = (e.get('source'), e.get('xref_id'), e.get('xref_name'), e.get('url'))
            if key in seen:
                continue
            seen.add(key)
            # strip None fields for cleanliness
            out.append({k: v for k, v in e.items() if v is not None})

        self._cross_references = out

    def _parseTargetComponents(self):
        """
        Parse target components.
        Populates: self._target_components → list of dicts with:
        accession, component_id, component_type, component_description, organism,
        synonyms=[{synonym, syn_type}], go_slims=[{go_id, label, aspect}],
        protein_classifications=[{path, raw}]
        """
        comps_out = []
        # target_components -> target_component -> ...
        for tcs in self._children(self._rawdata, 'target_components'):
            for comp in self._children(tcs, 'target_component'):
                entry = {
                    'accession': self._str(comp, 'accession'),
                    'component_id': self._str(comp, 'component_id'),
                    'component_type': self._str(comp, 'component_type'),
                    'component_description': self._str(comp, 'component_description'),
                    'relationship': self._str(comp, 'relationship'),
                    'synonyms': [],
                    'xrefs': [],
                }

                # target_component_synonym
                for syn_block in self._children(comp, 'target_component_synonyms'):
                    for syn in self._children(syn_block, 'target_component_synonym'):
                        entry['synonyms'].append({
                            'synonym': self._str(syn, 'component_synonym'),
                            'syn_type': self._str(syn, 'syn_type'),
                        })

                # target_component_xrefs
                # --- xrefs: target_component_xrefs -> (target_component_xref | target)
                for xrefs_block in self._children(comp, 'target_component_xrefs'):
                    # Support both child tag styles:
                    #    A) 'target_component_xref   N': { xref_id, xref_name, xref_src_db, xref_url }
                    #    B) 'target   N'              : { xref_id, xref_name, xref_src_db, xref_url }
                    xref_children = []
                    xref_children.extend(self._children(xrefs_block, 'target_component_xref'))
                    xref_children.extend(self._children(xrefs_block, 'target'))  # <-- your PDBe example

                    for x in xref_children:
                        src  = self._str(x, 'xref_src_db') or self._str(x, 'xref_src')
                        xid  = self._str(x, 'xref_id')
                        xnm  = self._str(x, 'xref_name')   # e.g., chain 'A'
                        if src or xid or xnm:
                            entry['xrefs'].append({'source': src, 'xref_id': xid, 'xref_name': xnm})

                comps_out.append(entry)

        self._target_components = comps_out

    def _parse(self):
        self._parseCrossReferences()
        self._parseCrossReferences()
        self._parseTargetComponents()

def queryChembl(id):
    if not isinstance(id, str):
        raise TypeError('id should be a string')

    try:
        record_file = openURL('https://www.ebi.ac.uk/chembl/api/data/target/{0}?format=xml'.format(id))
    except:
        raise ValueError('No Uniprot record found with that id')
        
    data = record_file.read()
    record_file.close()
    data = XML(data)

    return ALLdictElement(dictElement(data, prefix=None, number_multiples=True),
                         prefix=None, number_multiples=True)

def searchChembl(id):
    """Search Uniprot with *id* and return a :class:`UniprotRecord` containing the results. 
    """
    def _queryChembl(*args, n_attempts=3, dt=1, **kwargs):
        """
        Redefine prody function to check for no internet connection
        """
        attempt = 0
        while attempt < n_attempts:
            try:
                _ = openURL('https://www.ebi.ac.uk/chembl/')
                break
            except:
                LOGGER.info(
                    f'Attempt {attempt} to contact https://www.ebi.ac.uk/chembl/ failed')
                attempt += 1
                time.sleep((attempt+1)*dt)
        else:
            _ = openURL('https://www.ebi.ac.uk/chembl/')
        return queryChembl(*args, **kwargs)
    data = _queryChembl(id)
    return ChemblRecord(data)