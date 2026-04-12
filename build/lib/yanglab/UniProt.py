"""This module defines a class and relative functions for parsing Uniprot
information and corresponding PDB.

Some important definitions should be acknowledged. 

Reference: https://www.rcsb.org/docs/general-help/identifiers-in-pdb
1. PDB entity: (Entity level Identifier)
An entity is a chemically distinct part of a structure. One entry may have multiple copies (instances) of a given entity

2. PDB instance: (Instance level Identifiers)
An instance is a distinct copy of an entity or molecule.

For example, a heterotetramer hemoglobin (4hhb) contains two copies of the hemoglobin alpha chain (or chains A and C) 
and two copies of the beta chain (or chains B and D). People then name it as follow:
- the hemoglobin alpha: entity 1 --> chains A and C: instances A and C
- the hemoglobin beta: entity 2 --> chains B and D: instances B and D
"""

import time
import re
import os 
import json
import pandas as pd 

from xml.etree.cElementTree import XML
from rcsbapi.data import DataQuery as Query
from rcsbapi.search import AttributeQuery, NestedAttributeQuery

from .utils.logger import LOGGER
from .utils.tools import openURL, dictElement, dictElementLoop
from .RCSB import fetchLigands, fetchMetadata, fetchSeqAnnot, queryUid2RCSB
from .RCSB import align_RCSB2UniProt, fetchOligosaccharides


comma_splitter = re.compile(r'\s*,\s*').split
ns = {'up': 'http://uniprot.org/uniprot'}

COFACTOR = {
    'CHEBI:17996': ['CL'], # chloride
    'CHEBI:18420': ['MG'], # Mg(2+)
    'CHEBI:25516': ['NI'], # Ni cation
    'CHEBI:29033': ['FE2'],# Fe(2+)
    'CHEBI:24875': ['FE2', 'FE'], # Fe cation
    'CHEBI:29035': ['MN'], # Mn(2+)
    'CHEBI:29036': ['CU'], # Cu(2+)
    'CHEBI:29101': ['NA'],  # Na(+)
    'CHEBI:29103': ['K'],  # K(+)
    'CHEBI:29105': ['ZN'],  # Zn(2+)
    'CHEBI:29108': ['CA'],  # Ca(2+)
    'CHEBI:60240': ['FE2', 'MN', 'CA', 'CU', 'MG', 'NI', 'ZN'], # a divalent metal cation
    'CHEBI:30413': ['HEM'], # heme
    'CHEBI:60344': ['COH', 'HEB'], # heme b
    'CHEBI:190135':['FES'], # [2Fe-2S] cluster
    'CHEBI:49883': ['SF4'],     # [4Fe-4S] cluster
    'CHEBI:71302': ['MOM', 'MTE'], # Mo-molybdopterin
    'CHEBI:57692': ['FAD'], # FAD
    'CHEBI:58210': ['FMN'], # FMN
    'CHEBI:58937': ['TPP'], # thiamine diphosphate
    'CHEBI:597326': ['PLP'], # pyridoxal 5'-phosphate
    'CHEBI:unk_0': ['NAD', 'NDP', 'NAP'], # NICOTINAMIDE-ADENINE-DINUCLEOTIDE
    'CHEBI:unk_1': ['COA'], # COENZYME A
    'CHEBI:unk_2': ['B1Z', 'B12'], # Adenosylcobalamin or COBALAMIN # 5'-Deoxyadenosylcobalamin (vitamin B12)
    'CHEBI:unk_3': ['BTN'], # Biotin (biocytin)
    'CHEBI:unk_4': ['THG'], # Tetrahydrofolate (THF)
}

COFACTOR_COENZYME = ['FAD', 'FMN', 'TPP', 'PLP', 'NAD', 'NDP', 'NAP', 'COA', 'B1Z', 'B12', 'BTN', 'THG']
class UniprotRecord(object):
    """Wrapper for UniProt data with methods for accessing fields and parsing related PDB entries."""
    
    def __init__(self, data):
        self._rawdata = data
        self._pdbdata = []
        self._parse()
            
    def __repr__(self):
        return '<UniprotRecord: %s>' % self.getTitle()

    def __str__(self):
        return self.getTitle()

    def getXML(self):
        return f'http://www.uniprot.org/uniprot/{0}.xml'.format(self.getAccession())

    def setData(self, value):
        self._rawdata = value
        self._parse()

    def getData(self):
        return self._rawdata

    def getPDBs(self):
        return self._pdbdata

    def getAccession(self, index=0):
        """Get primary accession."""
        return self.getEntry('accession', index)

    def getName(self, index=0):
        """Get entry name."""
        return self.getEntry('name', index)

    def getProtein(self, index=0):
        """Get recommended and alternative protein names."""
        protein = self.getEntry('protein', index)
        try:
            recommend_elem = protein.find('up:recommendedName', ns)
            alternative_elem = protein.find('up:submittedName', ns)
            
            recommend_name = recommend_elem.find('up:fullName', ns) if recommend_elem is not None else None
            alter_fullname = alternative_elem.find('up:fullName', ns) if alternative_elem is not None else None
            alter_shortname = alternative_elem.find('up:shortName', ns) if alternative_elem is not None else None
            
            recommend_name = recommend_name.text if recommend_name is not None else None
            alter_fullname = alter_fullname.text if alter_fullname is not None else None
            alter_shortname = alter_shortname.text if alter_shortname is not None else None
        except:
            # Fallback if structure differs
            submitted_name = protein.find('up:submittedName/up:fullName', ns)
            recommend_name = submitted_name.text if submitted_name is not None else None
            alter_fullname = None
            alter_shortname = None
        
        return {
            'recommend_name': recommend_name,
            'alter_fullname': alter_fullname,
            'alter_shortname': alter_shortname            
        }

    def getGene(self, index=0):
        """Get primary gene name."""
        try:
            gene = self.getEntry('gene', index)
            name_elem = gene.find('up:name[@type="primary"]', ns)
            return name_elem.text if name_elem is not None else None
        except Exception as e:
            LOGGER.warn(f'Error parsing gene name: {e}')
            return None

    def getOrganism(self, index=0):
        """Get organism scientific and common names, taxonomy."""
        organism = self.getEntry('organism', index)
        sci_name = organism.find('up:name[@type="scientific"]', ns)
        com_name = organism.find('up:name[@type="common"]', ns)
        db_ref = organism.find('up:dbReference[@type="NCBI Taxonomy"]', ns)
        lineage_tags = organism.findall('up:lineage/up:taxon', ns)
        return {
            'scientific_name': sci_name.text.strip() if sci_name is not None else None,
            'common_name': com_name.text.strip() if com_name is not None else None,
            'taxonomy_id': db_ref.attrib['id'] if db_ref is not None else None,
            'lineage': [taxon.text.strip() for taxon in lineage_tags if taxon.text]
        }

    def getSequence(self, index=0):
        return self.getEntry('sequence', index)

    def getCellLocation(self):
        return self._cell_location

    def getDNAbinding(self):
        return self._dna_binding

    def getZincFinger(self):
        return self._zinc_finger

    def getActiveSite(self):
        return self._active_site

    def getBindingSite(self):
        return self._binding_site

    def getSite(self):
        return self._site

    def getAlphaFold(self):
        """Return AlphaFold DB ID if present."""
        AlphaFoldDB = None
        for key, value in self._rawdata.items():
            if not key.startswith('dbReference'):
                continue
            if type(value) != list or len(value) != 2:
                continue
            # List like: [('type','AlphaFoldDB'), ('id','QXXXXX')]
            if value[0][1] == 'AlphaFoldDB':
                AlphaFoldDB = value[1][1]
                break
        return AlphaFoldDB

    def getCofactor(self):
        return self._cofactors

    # New getters for additional parsed features:
    def getPTMProcessing(self):
        return self._ptm_processing

    def getInteractions(self):
        return self._interactions

    def getFamilyDomains(self):
        return self._family_domains

    def getComplexPortals(self):
        """Return list of complex names from ComplexPortal references."""
        return self._complex_portals

    def getSubunit(self, kind: str = 'all'):
        """
        Return subunit comment texts.
        kind: 'all' | 'microbial' | 'non_microbial'
        """
        if not hasattr(self, '_subunit_comments'):
            # Not parsed yet (older instances)? parse now.
            self._parseSubunit()
        kind = (kind or 'all').lower()
        if kind not in ('all', 'microbial', 'non_microbial'):
            kind = 'all'
        return self._subunit_comments.get(kind, [])

    def getTitle(self):
        uid = self.getAccession()
        name = self.getName()
        return f'{uid} ({name})'

    def getEntry(self, item, index=0):
        key = f'{item}{index:4d}'
        if key in self._rawdata:
            return self._rawdata[key]
        else:
            raise KeyError(f'{item} does not exist in the record')

    def _parseDNAbinding(self):
        data = self._rawdata
        dna_binding = []
        for key, value in data.items():
            if not key.startswith('feature'):
                continue
            if value.get('type') != "DNA-binding region":
                continue
            descp = value.get('description')
            begin_elem = value.find('up:location/up:begin', ns)
            end_elem = value.find('up:location/up:end', ns)
            begin = begin_elem.attrib.get('position') if begin_elem is not None else None
            end = end_elem.attrib.get('position') if end_elem is not None else None
            dna_binding.append({'description': descp, 'begin': begin, 'end': end})
        self._dna_binding = dna_binding

    def _parseZincfinger(self):
        data = self._rawdata
        zinc_finger = []
        for key, value in data.items():
            if not key.startswith('feature'):
                continue
            if value.get('type') != "zinc finger region":
                continue
            descp = value.get('description')
            begin_elem = value.find('up:location/up:begin', ns)
            end_elem = value.find('up:location/up:end', ns)
            begin = begin_elem.attrib.get('position') if begin_elem is not None else None
            end = end_elem.attrib.get('position') if end_elem is not None else None
            zinc_finger.append({'description': descp, 'begin': begin, 'end': end})
        self._zinc_finger = zinc_finger

    def _parseActiveSite(self):
        data = self._rawdata
        active_site = []
        for key, value in data.items():
            if not key.startswith('feature'):
                continue
            if value.get('type') != "active site":
                continue
            descp = value.get('description')
            pos_elem = value.find('up:location/up:position', ns)
            pos = int(pos_elem.attrib.get('position')) if pos_elem is not None else None
            active_site.append({'description': descp, 'position': pos})
        self._active_site = active_site

    def _parseBindingSite(self):
        data = self._rawdata
        binding_site = []
        for key, value in data.items():
            if not key.startswith('feature'):
                continue
            if value.get('type') != "binding site":
                continue
            descp = value.get('description', None)
            loc_elem = value.find('up:location', ns)
            pos_elem = loc_elem.find('up:position', ns)
            begin_elem = loc_elem.find('up:begin', ns)
            end_elem = loc_elem.find('up:end', ns)
            if pos_elem is None:
                pos = f"{begin_elem.attrib.get('position')}-{end_elem.attrib.get('position')}"
            else:
                pos = pos_elem.attrib.get('position')
            ligand_elem = value.find('up:ligand', ns)
            ligand_name = ligand_elem.find('up:name', ns)
            ligand_name = ligand_name.text if ligand_name is not None else None
            ligand_chebi = ligand_elem.find('up:dbReference[@type=\"ChEBI\"]', ns)
            ligand_chebi = ligand_chebi.attrib['id'] if ligand_chebi is not None else None
            binding_site.append({
                'position': pos,
                'description': descp,
                'name': ligand_name,
                'chebi': ligand_chebi
            })
        self._binding_site = binding_site

    def _parseSite(self):
        data = self._rawdata
        site = []
        for key, value in data.items():
            if not key.startswith('feature'):
                continue
            if value.get('type') != "site":
                continue
            descp = value.get('description')
            loc_elem = value.find('up:location', ns)
            pos_elem = loc_elem.find('up:position', ns)
            begin_elem = loc_elem.find('up:begin', ns)
            end_elem = loc_elem.find('up:end', ns)
            if pos_elem is None:
                pos = f"{begin_elem.attrib.get('position')}-{end_elem.attrib.get('position')}"
            else:
                pos = pos_elem.attrib.get('position')
            site.append({'position': pos, 'description': descp})
        self._site = site

    def _parseCofactor(self):
        data = self._rawdata
        cofactors = []
        for key, value in data.items():
            if not key.startswith('comment'):
                continue
            if type(value) == list:
                continue
            if value.get('type') != "cofactor":
                continue
            cf_elem = value.find('up:cofactor', ns)
            cf_name = cf_elem.find('up:name', ns)
            cf_chebi = cf_elem.find('up:dbReference[@type=\"ChEBI\"]', ns)
            cf_chebi = cf_chebi.attrib['id'] if cf_chebi is not None else None
            cofactors.append({
                'name': cf_name.text,
                'chebi': cf_chebi
            })
        self._cofactors = cofactors

    def _parseCellLocation(self):
        data = self._rawdata
        cell_location = []
        for key, value in data.items():
            if not key.startswith('feature'):
                continue
            loc_type = value.get('type')
            if loc_type not in ['topological domain', 'transmembrane region', 'intramembrane region']:
                continue
            descp = value.get('description')
            begin_elem = value.find('up:location/up:begin', ns)
            end_elem = value.find('up:location/up:end', ns)
            begin = begin_elem.attrib.get('position') if begin_elem is not None else None
            end = end_elem.attrib.get('position') if end_elem is not None else None
            cell_location.append({
                'type': loc_type,
                'description': descp,
                'begin': begin,
                'end': end
            })
        self._cell_location = cell_location

    def _parsePTMProcessing(self):
        data = self._rawdata
        ptms = []
        types_of_interest = ["signal peptide", "transit peptide", "chain", "propeptide", "peptide",
                             "disulfide bond", "glycosylation site", "modified residue", "lipidation site"]
        for key, value in data.items():
            if not key.startswith('feature'):
                continue
            type_ = value.get('type')
            if type_ not in types_of_interest:
                continue
            descp = value.get('description')
            loc_elem = value.find('up:location', ns)
            if loc_elem is None:
                continue
            pos_elem = loc_elem.find('up:position', ns)
            begin_elem = loc_elem.find('up:begin', ns)
            end_elem = loc_elem.find('up:end', ns)
            if pos_elem is not None:
                pos = pos_elem.attrib.get('position')
                ptms.append({'type': type_, 'position': pos, 'description': descp})
            else:
                begin = begin_elem.attrib.get('position') if begin_elem is not None else None
                end = end_elem.attrib.get('position') if end_elem is not None else None
                ptms.append({'type': type_, 'begin': begin, 'end': end, 'description': descp})
        self._ptm_processing = ptms

    def _parseComplexPortals(self):
        """Return the list of ComplexPortal complex names."""
        data = self._rawdata
        self._complex_portals = []

        for key, value in data.items():
            if not key.startswith('dbReference'):
                continue

            if type(value) is list or type(value) is dict:
                continue

            if value.get('type') != 'ComplexPortal':
                continue
            
            cp_id = value.get('id')
            property_elem = value.find('up:property', ns)
            if property_elem is None:
                continue
            name = property_elem.get('value')
            self._complex_portals.append(
                {
                    'id': cp_id,
                    'name': name
                }
            )

    def _parseSubunit(self):
        """
        Collect all <comment type="subunit"><text>...</text></comment> entries from the UniProt XML.
        Stores a dict with keys:
            - 'all': list of all text strings
            - 'microbial': list of texts that start with or contain '(Microbial infection)'
            - 'non_microbial': list of the rest
        """
        data = self._rawdata
        subunit_all = []

        # Some parsers store XML Elements in self._rawdata['comment....']
        # We iterate through them similarly to _parseInteractions.
        for key, value in data.items():
            if not key.startswith('comment'):
                continue

            # Sometimes value could be a list; iterate through if so
            values = value if isinstance(value, list) else [value]

            for v in values:
                try:
                    vtype = v.get('type')
                except AttributeError:
                    # not an XML element
                    continue

                if vtype != 'subunit':
                    continue

                # Namespace-aware search for <text>
                try:
                    text_elem = v.find('up:text', ns)  # ns is defined at module-level
                except Exception:
                    text_elem = None

                if text_elem is not None and text_elem.text:
                    txt = text_elem.text.strip()
                    if txt:
                        subunit_all.append(txt)

        microbial = [t for t in subunit_all if '(Microbial infection)' in t]
        non_micro = [t for t in subunit_all if '(Microbial infection)' not in t]

        self._subunit_comments = {
            'all': subunit_all,
            'microbial': microbial,
            'non_microbial': non_micro,
        }

    def _parseFamilyDomains(self):
        data = self._rawdata
        family_domains = []
        types_of_interest = [
            "domain", "region of interest", "coiled-coil region", 
            "short sequence motif", "repeat"
        ]
        for key, value in data.items():
            if not key.startswith('feature'):
                continue
            type_ = value.get('type')
            if type_ not in types_of_interest:
                continue
            descp = value.get('description')
            loc_elem = value.find('up:location', ns)
            if loc_elem is None:
                continue
            begin_elem = loc_elem.find('up:begin', ns)
            end_elem = loc_elem.find('up:end', ns)
            begin = begin_elem.attrib.get('position') if begin_elem is not None else None
            end = end_elem.attrib.get('position') if end_elem is not None else None
            family_domains.append({'type': type_, 'description': descp, 'begin': begin, 'end': end})
        self._family_domains = family_domains

    def _parseInteractions(self):
        data = self._rawdata
        interactions = []
        self_acc = self.getAccession()
        for key, value in data.items():
            if not key.startswith('comment'):
                continue
            if type(value) == list:
                continue
            if value.get('type') != "interaction":
                continue
            interactants = value.findall('up:interactant', ns)
            for ia in interactants:
                ia_id_elem = ia.find('up:id', ns)
                if ia_id_elem is None:
                    continue
                ia_id = ia_id_elem.text
                label_elem = ia.find('up:label', ns)
                ia_label = label_elem.text if label_elem is not None else None
                if ia_id != self_acc:
                    interactions.append({'id': ia_id, 'label': ia_label})
        self._interactions = interactions

    def fetchPDBfromRCSB(self):
        uid = self.getAccession()
        data = queryUid2RCSB(uid)
        if len(data) == 0:
            LOGGER.warn(f'No PDB structure')
            self._pdbdata = data
            return
        
        for pdbid in data:
            sample = data[pdbid]
            pdb_entity = sample['pdb_entity']
            align = align_RCSB2UniProt(pdb_entity, uid)
            if not align:
                continue

            sample['aligned_regions'] = align['aligned_regions']
            sample['query_seq'] = align['query_seq']

        pdblist = list(data.keys())
        ligands = fetchLigands(pdblist)
        olisacs = fetchOligosaccharides(pdblist)
        metadata = fetchMetadata(pdblist)

        for id in pdblist:
            pdb_inst = data[id]['pdb_instance']
            seqannot = fetchSeqAnnot(uid, pdb_inst)

            data[id]['ligand'] = ligands[id]
            data[id]['olisac'] = olisacs[id]
            data[id]["metadata"] = metadata
            data[id]['polymer_entities'] = metadata[id]["polymer_entities"]
            data[id]["seqannot"] = seqannot
        
        self._pdbdata = data

    def _parsePDBfromUniProt(self):
        data = self._rawdata
        PDBdata = {}
        for key, value in data.items():
            if not key.startswith('dbReference'):
                continue
            try:
                pdbid = value['PDB']
            except (KeyError, TypeError):
                continue
            method = value.get('method', None)
            pdbchains = value.get('chains', [])
            resolution = value.get('resolution', '1.00 A')
            resolution = float(resolution.split(' ')[0])
            chains = []
            resrange = None
            try:
                pdbchains_list = comma_splitter(pdbchains)
                for chain in pdbchains_list:
                    chids, resrange = chain.split('=')
                    chids = [chid.strip() for chid in chids.split('/')]
                    for chid in chids:
                        chains.append(chid)
            except Exception as e:
                LOGGER.warn(str(e))
                LOGGER.warn('Suspected no chain information')
            PDBdata[pdbid] = {
                'method': method,
                'resolution': resolution,
                'chains': chains,
                'resrange': resrange,
            }
        pdblist = list(PDBdata.keys())
        if not pdblist:
            self._pdbdata = PDBdata
            return
        ligands = fetchLigands(pdblist)
        rvalues = fetchMetadata(pdblist)
        auth2label = self.fetchAsymIDs(pdblist)
        for pdbid in PDBdata:
            PDBdata[pdbid]['ligand'] = ligands.get(pdbid)
            rval = rvalues.get(pdbid, {})
            PDBdata[pdbid]['initial_release_date'] = rval.get('initial_release_date')
            PDBdata[pdbid]['ls_R_factor_R_free'] = rval.get('ls_R_factor_R_free')
            PDBdata[pdbid]['ls_R_factor_R_work'] = rval.get('ls_R_factor_R_work')
            PDBdata[pdbid]['ls_R_factor_obs'] = rval.get('ls_R_factor_obs')
            chains = PDBdata[pdbid]['chains']
            asym_record = auth2label.get(pdbid, [])
            if asym_record:
                chains = [next((rec['label_asym_id'] for rec in asym_record if rec['auth_asym_id'] == chid), chid) for chid in chains]
            pdb_instances = [f'{pdbid}.{chid}' for chid in chains]
            seq_annot = fetchSeqAnnot(self.getAccession(), pdb_instances) if pdb_instances else None
            PDBdata[pdbid]['seq_annot'] = seq_annot
        self._pdbdata = PDBdata

    def fetchAsymIDs(self, pdblist):
        """
        Convert auth_asym_ids to label_asym_id.
        """
        q = Query(
            input_type="entries",
            input_ids=pdblist,
            return_data_list=[
                "rcsb_id",
                "polymer_entities.polymer_entity_instances.rcsb_id",
                "polymer_entities.polymer_entity_instances.rcsb_polymer_entity_instance_container_identifiers.auth_asym_id",
                "polymer_entities.polymer_entity_instances.rcsb_polymer_entity_instance_container_identifiers.asym_id",
                "polymer_entities.polymer_entity_instances.rcsb_polymer_entity_instance_container_identifiers.entity_id",
            ]
        )
        r = q.exec()
        auth2label = {}
        for entry in r['data']['entries']:
            pdbid = entry['rcsb_id']
            asym_record = []
            for entity in entry['polymer_entities']:
                for inst in entity['polymer_entity_instances']:
                    asym_record.append({
                        'rcsb_id': inst['rcsb_id'],
                        'auth_asym_id': inst['rcsb_polymer_entity_instance_container_identifiers']['auth_asym_id'],
                        'label_asym_id': inst['rcsb_polymer_entity_instance_container_identifiers']['asym_id'],
                        'entity_id': inst['rcsb_polymer_entity_instance_container_identifiers']['entity_id'],
                    })
            auth2label[pdbid] = asym_record
        return auth2label

    def _parse(self):
        acc = self.getAccession()
        LOGGER.info(f'Parse UniProt information of {acc}...')
        LOGGER.timeit('_parse')
        self._parseActiveSite()
        self._parseBindingSite()
        self._parseSite()
        self._parseCofactor()
        self._parseDNAbinding()
        self._parseZincfinger()
        self._parseCellLocation()
        self._parsePTMProcessing()
        self._parseFamilyDomains()
        self._parseInteractions()
        self._parseComplexPortals()
        self.fetchPDBfromRCSB()
        self._parseSubunit()
        LOGGER.report(f'Parsing in %.1fs.', '_parse')
        
def queryUniprot(id, expand=[], regex=True):
    """Query Uniprot with *id* and return a `dict` containing the raw results. 
    Regular users should use :func:`searchUniprot` instead.
    
    :arg expand: entries through which you want to loop dictElements
        until there aren't any elements left
    :type expand: list
    """

    if not isinstance(id, str):
        raise TypeError('id should be a string')

    try:
        record_file = openURL('http://www.uniprot.org/uniprot/{0}.xml'.format(id))
    except:
        raise ValueError('No Uniprot record found with that id')
    
    data = record_file.read()
    record_file.close()
    data = XML(data)

    data = dictElement(data[0], '{http://uniprot.org/uniprot}', number_multiples=True)

    for key in data:
        value = data[key]
        if not key.startswith('dbReference'):
            continue
        
        try:
            if value.get('type') != 'PDB':
                continue
        except AttributeError:
            continue

        pdbid = value.get('id')
        refdata = {'PDB': pdbid}
        for prop in value:
            prop_key = prop.get('type')
            prop_val = prop.get('value')
            refdata[prop_key] = prop_val
        data[key] = refdata
            
    if expand:
        keys = []
        if regex:
            for lt in expand:
                lt_re = re.compile(lt)
                for key in data:
                    if lt_re.match(key):
                        keys.append(key)
        else:
            keys = expand
        data = dictElementLoop(data, keys, '{http://uniprot.org/uniprot}')
    
    return data

def searchUniprot(id):
    """Search Uniprot with *id* and return a :class:`UniprotRecord` containing the results. 
    """
    def _queryUniprot(*args, n_attempts=3, dt=1, **kwargs):
        """
        Redefine prody function to check for no internet connection
        """
        attempt = 0
        while attempt < n_attempts:
            try:
                _ = openURL('http://www.uniprot.org/')
                break
            except:
                LOGGER.info(
                    f'Attempt {attempt} to contact www.uniprot.org failed')
                attempt += 1
                time.sleep((attempt+1)*dt)
        else:
            _ = openURL('http://www.uniprot.org/')
        return queryUniprot(*args, **kwargs)

    data = _queryUniprot(id)
    return UniprotRecord(data)

def filter_essence(entry: dict) -> dict:
    """
    Flatten the parsed UniProt dict into easy-to-use columns.
    Same as before, except `interactions` now becomes a simple list of partner IDs.
    """

    # ---- helpers ----
    def as_list(x):
        return x if isinstance(x, list) else ([] if x is None else [x])

    def fmt_range(d):
        if not isinstance(d, dict):
            return None
        if d.get("position") is not None:
            return str(d["position"])
        b, e = d.get("begin"), d.get("end")
        if b is not None and e is not None:
            return f"{b}-{e}"
        return None

    # ---- basics ----
    uid = entry.get("id")
    prot = entry.get("protein") or {}
    protein_name = prot.get("recommend_name") or prot.get("alter_fullname") or entry.get("protein")
    gene = entry.get("gene")
    org_block = entry.get("organism") or {}
    organism = org_block.get("common_name") or org_block.get("scientific_name")

    # ---- functional sites (simple lists) ----
    binding_site = [str(s.get("position")) for s in as_list(entry.get("binding_site")) if s.get("position") is not None]
    active_site  = [str(s.get("position")) for s in as_list(entry.get("active_site"))  if s.get("position") is not None]
    site         = [str(s.get("position")) for s in as_list(entry.get("site"))         if s.get("position") is not None]
    dna_binding  = [r for r in (fmt_range(d) for d in as_list(entry.get("dna_binding"))) if r]
    zinc_finger  = [r for r in (fmt_range(d) for d in as_list(entry.get("zinc_finger"))) if r]

    # ---- cellular location ----
    intra_mem, topol_dom, trans_mem = [], [], []
    for loc in as_list(entry.get("cell_location")):
        t = (loc.get("type") or "").lower()
        r = fmt_range(loc)
        if not r:
            continue
        if t == "intramembrane region":
            intra_mem.append(r)
        elif t == "topological domain":
            topol_dom.append(r)
        elif t == "transmembrane region":
            trans_mem.append(r)

    # ---- PTM / Processing ----
    ptm_processing = []
    for f in as_list(entry.get("ptm")):
        ptm_processing.append({
            "type": f.get("type"),
            "description": f.get("description"),
            "location": fmt_range(f),
        })

    # ---- Family & Domains ----
    family_domains = []
    for f in as_list(entry.get("family_domains") or entry.get("fadomain")):
        family_domains.append({
            "type": f.get("type"),
            "description": f.get("description"),
            "location": fmt_range(f),
        })

    # ---- ComplexPortal ----
    complex_portal = []
    for c in as_list(entry.get("complex_portal") or entry.get("complex_viewer")):
        if isinstance(c, dict):
            complex_portal.append({"id": c.get("id"), "name": c.get("name")})
        else:
            complex_portal.append({"id": None, "name": str(c)})

    # ---- Interactions -> just partner IDs (dedup, preserve order) ----
    raw_inter = entry.get("interactions") if "interactions" in entry else entry.get("interaction")
    partners = []
    for it in as_list(raw_inter):
        if isinstance(it, dict):
            p = it.get("partner") or it.get("accession") or it.get("id")
            if p:
                partners.append(str(p))
        else:
            partners.append(str(it))
    # deduplicate preserving order
    partners = list(dict.fromkeys(partners))

    # ---- PDB (keep block as-is unless you post-process elsewhere) ----
    pdb_block  = entry.get("pdb") or {}
    pdb_list = list(pdb_block.keys())
    alphafold  = entry.get("alphafold")

    return {
        "id": uid,
        "protein": protein_name,
        "gene": gene,
        "organism": organism,
        "uni_cofactor": entry.get("uni_cofactor") or entry.get("cofactor") or [],

        "intra_mem": intra_mem,
        "topol_dom": topol_dom,
        "trans_mem": trans_mem,

        "binding_site": binding_site,
        "active_site": active_site,
        "site": site,
        "dna_binding": dna_binding,
        "zinc_finger": zinc_finger,

        "ptm_processing": ptm_processing,
        "family_domains": family_domains,
        "complex_portal": complex_portal,

        # simplified interactions
        "interactions": partners,

        "pdb": pdb_list,
        "alphafold": alphafold,
    }

def dump_csv(data, filename, folder):
    # --- paths ---
    out_csv = os.path.join(folder, filename)
    os.makedirs(folder, exist_ok=True)
    # --- helper: join simple lists, JSON-encode complex ones ---
    def _join_list(x):
        if x is None:
            return ""
        if isinstance(x, list):
            # simple list of scalars -> join
            if all(not isinstance(i, (dict, list)) for i in x):
                return "|".join(str(i) for i in x if i not in ("", None))
        # otherwise leave to json.dumps in the converter below
        return x
    def _to_json(x):
        # JSON-encode non-empty complex fields (list/dict); empty -> ""
        if x in (None, [], {}):
            return ""
        return json.dumps(x, ensure_ascii=False)
    # --- run filter_essence and collect rows ---
    rows = []
    for e in data:
        try:
            row = filter_essence(e)  # <-- reusing your function
            rows.append(row)
        except Exception as ex:
            # skip bad records but keep going
            print(f"[WARN] Skipping record {e.get('id', '<unknown>')}: {ex}")
    df = pd.DataFrame(rows)
    # --- make columns easy to read ---
    # 1) simple list-of-strings columns: join with "|"
    simple_list_cols = [
        "binding_site", "active_site", "site",
        "dna_binding", "zinc_finger",
        "intra_mem", "topol_dom", "trans_mem",
        "pdb_ids", "pdb_methods", "pdb_ligands",
    ]
    for c in simple_list_cols:
        if c in df.columns:
            df[c] = df[c].apply(_join_list)
    # 2) structured/list-of-dicts columns: JSON-encode into a single cell
    structured_cols = [
        "ptm_processing", "family_domains",
        "complex_portal", "interactions",
    ]
    for c in structured_cols:
        if c in df.columns:
            df[c] = df[c].apply(_to_json)
    # --- write CSV ---
    df.to_csv(out_csv, index=False)
    print(f"Done. Wrote {len(df)} rows to {out_csv}")
    return df


def pickPDBfromUniprot(entry, to_file=None):
    data = filter_essence(entry)
    id = data['id'] # uniprot id
    seq_len = len(data['sequence']) # uniprot protein length
    
    # Cofactor
    uni_cofactor = data['uni_cofactor']
    uni_cofactor_chebi = [cf['chebi'] for cf in uni_cofactor]
    uni_cofactor_id = []
    for l in uni_cofactor_chebi:
        uni_cofactor_id.extend(COFACTOR[l])
    if len(uni_cofactor_id) == 0:
        LOGGER.info(f"{id}, no cofactor")
    else: 
        LOGGER.info(f"{id}, cofactor(s):")
        for i, cof in enumerate(uni_cofactor):
            LOGGER.info(f"{cof['name']}, {cof['chebi']}, {uni_cofactor_id[i]}")
    
    # Functional site
    _func_site_ = []
    for sname in ['active_site', 'binding_site', 'dna_binding', 'zinc_finger']:
        _site = data[sname]
        if len(_site) != 0:
            _func_site_.extend(_site)
            LOGGER.info(f"{sname}: {_site}")
    
    # lst = ['280', '99-101', '103-105']
    # out: [280, 99, 100, 101, 103, 104, 105]
    func_site = []
    for item in _func_site_:
        item = str(item)
        if '-' in item:
            start, end = map(int, item.split('-'))
            func_site.extend(range(start, end + 1))
        else:
            func_site.append(int(item))
    
    # PDB structures
    pdb = data.get('pdb')
    if len(pdb) == 0:
        LOGGER.warn(f"{id} has no PDB structures")
    
    # Retrieve key information to rank PDB structures
    PDBrank = []
    for pdbid, entry in pdb.items():
        resolution = entry['resolution']
        pdb_ligand = entry['ligand']
        r_free = entry['ls_R_factor_R_free']
        seq_annot = entry['seq_annot']
        resrange = entry['resrange']
        
        # Retrieve ligand id
        if pdb_ligand is not None:
            pdb_ligand_id = [l['comp_id'] for l in pdb_ligand]
        else:
            pdb_ligand_id = []
            
        # Count number of _cofactors = cofactor coenzyme + cofactor ion
        # Count number of (ligands+drugs) other than _cofactors
        _cofactors = set(pdb_ligand_id).intersection(set(uni_cofactor_id))
        _coenzymes = set(pdb_ligand_id).intersection(set(COFACTOR_COENZYME))
        _cofactors = _cofactors.union(_coenzymes)
        _ligands_or_drugs = set(pdb_ligand_id).difference(set(uni_cofactor_id))
        
        # resolved_len with respect to uniprot sequence e.g., '100-250'
        if resrange is None:
            resolved_len = 0
            LOGGER.warn(f"{pdbid} has no resolved range")
        else:
            _split = resrange.split('-')
            resolved_len = int(_split[1]) - int(_split[0]) + 1
        
        # Iterate each chain (instance) recorded in uniprot
        for inst_id, value in seq_annot.items():
            n_mut = value['rcsb_mutation_count']
            bas_id = value['biological_assembly']
            
            # dict, key: missing pdb resID, value: uniprot ID 
            # e.g., (1, 12): [(24, 30)] 
            mapped = value['mapped'] 
            
            # modeled_len is resolved_len substracted missing residues
            n_missing_res = 0
            n_missing_fsite = 0
            for _, m in mapped.items():
                if len(m) == 0:
                    continue
                _range = m[0]
                missing_range = range(_range[0], _range[1])
                missing_fsite = set(func_site).intersection(set(missing_range))
                n_missing_res += len(missing_range)
                n_missing_fsite += len(missing_fsite)
                
            modeled_len = resolved_len - n_missing_res
            coverage = modeled_len / seq_len
            PDBrank.append(
                (
                    id, uni_cofactor_id, seq_len, # 0, 1, 2
                    pdbid, inst_id, bas_id, pdb_ligand_id, # 3, 4, 5, 6
                    _cofactors, len(_cofactors), # 7, 8
                    _ligands_or_drugs, len(_ligands_or_drugs), # 9, 10
                    resrange, modeled_len, n_mut, n_missing_fsite, coverage, # 11, 12, 13, 14, 15
                    resolution, r_free # 16, 17
                )
            )
    # len(_cofactors) → n_missing_fsite → n_mut →
    # coverage → resolution → r_free →
    # len(_ligands_or_drugs)
    PDBrank.sort(key=lambda x: (-x[8], -x[14], x[13], 
                                -x[15], x[16], x[17], 
                                x[10])) # Smallest score first    
    # Save to csv file
    if to_file is not None:
        import pandas as pd 
        columns = [
            'id', 'uni_cofactor', 'uni_seq_len',
            'pdbid', 'chid', 'basid', 'all_pdb_ligands',
            'pdb_cofactors', 'n_pdb_cofactors', 
            'pdb_ligand_or_drugs', 'n_pdb_ligand_or_drugs',
            'resrange', 'modeled_len', 'n_mut', 'n_missing_fsite', 'coverage', 
            'resolution', 'r_free'
        ]
        df = pd.DataFrame(columns=columns, data=PDBrank)
        df.to_csv(to_file, index=False)
    return PDBrank
