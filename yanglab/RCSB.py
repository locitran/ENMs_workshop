"""
https://github.com/rcsb/py-rcsb-api

Data attributes for Data API
https://data.rcsb.org/data-attributes.html

"""

from rcsbapi.data import DataQuery as Query
from rcsbapi.search import AttributeQuery, NestedAttributeQuery
from rcsbapi.sequence import Alignments
from typing import Dict, List, Any
from collections import defaultdict
import prody

from .utils.logger import LOGGER
from .download import fetchPDB
from .proteins.ciffile import parseMMCIF

def fetchSeqAnnot(uid: str, pdb_instances: List[str]):
    """
    Fetch per-instance annotations and map unobserved PDB residue segments to UniProt ranges.

    Returns:
      {
        "<inst_id>": {
          "biological_assembly": [ "1", "2", ... ],
          "missing_segments": [ {"entity_beg": int, "entity_end": int}, ... ],
          "mapped_segments": [
              {
                  "entity_range": {"beg": int, "end": int},
                  "uniprot_ranges": [ {"beg": int, "end": int}, ... ]
              },
              ...
          ],
          "unobs_res_cov": float|int|None,
          "modeled_residue_count": int|None,
          "pdbx_mutation": str|None,
          "rcsb_mutation_count": int|None
        },
        ...
      }
    """
    def pdb2uniprot_ranges(beg: int, end: int, blocks: List[Dict[str, int]]):
        """
        Map an entity [beg,end] (1-based) to UniProt ranges using aligned blocks.
        blocks: list of {entity_beg_seq_id, ref_beg_seq_id, length}
        """
        out = []
        for b in (blocks or []):
            e0 = int(b.get("entity_beg_seq_id", 0))
            r0 = int(b.get("ref_beg_seq_id", 0))
            L  = int(b.get("length", 0))
            if L <= 0:
                continue
            e1 = e0 + L - 1
            s = max(beg, e0)
            t = min(end, e1)
            if s <= t:
                rs = r0 + (s - e0)
                rt = r0 + (t - e0)
                out.append({"beg": rs, "end": rt})
        return out

    q = Query(
        input_type="polymer_entity_instances",
        input_ids=pdb_instances,
        return_data_list=[
            "polymer_entity_instances.rcsb_id",
            "rcsb_polymer_instance_feature.type",
            "rcsb_polymer_instance_feature.feature_positions.beg_seq_id",
            "rcsb_polymer_instance_feature.feature_positions.end_seq_id",

            "polymer_entity.rcsb_polymer_entity_align.reference_database_name",
            "polymer_entity.rcsb_polymer_entity_align.reference_database_accession",
            "polymer_entity.rcsb_polymer_entity_align.aligned_regions.entity_beg_seq_id",
            "polymer_entity.rcsb_polymer_entity_align.aligned_regions.ref_beg_seq_id",
            "polymer_entity.rcsb_polymer_entity_align.aligned_regions.length",

            "polymer_entity.entry.rcsb_entry_container_identifiers.assembly_ids",
            "rcsb_polymer_instance_info.modeled_residue_count",
            "rcsb_polymer_instance_feature_summary.coverage",
            "rcsb_polymer_instance_feature_summary.type",
            "polymer_entity.rcsb_polymer_entity.pdbx_mutation",
            "polymer_entity.entity_poly.rcsb_mutation_count",
        ]
    )
    r = q.exec()
    out = {}

    for instance in (r.get("data", {}) or {}).get("polymer_entity_instances", []) or []:
        inst_id = instance.get("rcsb_id")
        if not inst_id:
            continue

        # Biological assembly IDs (list of strings)
        bas_ids = []
        try:
            bas_ids = instance.get("polymer_entity", {}) \
                              .get("entry", {}) \
                              .get("rcsb_entry_container_identifiers", {}) \
                              .get("assembly_ids") or []
        except Exception:
            bas_ids = []

        # Collect UNOBSERVED_RESIDUE_XYZ missing segments on the entity scale
        missing_segments: List[Dict[str, int]] = []
        for feat in instance.get("rcsb_polymer_instance_feature", []) or []:
            if feat.get("type") == "UNOBSERVED_RESIDUE_XYZ":
                for seg in feat.get("feature_positions", []) or []:
                    try:
                        b = int(seg.get("beg_seq_id"))
                        e = int(seg.get("end_seq_id"))
                        if b is not None and e is not None:
                            missing_segments.append({"entity_beg": b, "entity_end": e})
                    except Exception:
                        continue

        # Find alignment blocks to this UniProt accession
        aligned_blocks: List[Dict[str, int]] = []
        for ent in instance.get("polymer_entity", {}) \
                           .get("rcsb_polymer_entity_align", []) or []:
            if ent.get("reference_database_name") == "UniProt" and ent.get("reference_database_accession") == uid:
                aligned_blocks = ent.get("aligned_regions") or []
                break

        # Map each missing segment to UniProt ranges
        mapped_segments  = []
        for seg in missing_segments:
            beg, end = seg["entity_beg"], seg["entity_end"]
            uranges = pdb2uniprot_ranges(beg, end, aligned_blocks)
            mapped_segments.append({
                "entity_range": {"beg": beg, "end": end},
                "uniprot_ranges": uranges
            })

        # Coverage for unobserved residues
        unobs_res_cov = None
        for d in instance.get("rcsb_polymer_instance_feature_summary", []) or []:
            if d.get("type") == "UNOBSERVED_RESIDUE_XYZ":
                unobs_res_cov = d.get("coverage")
                break

        modeled_residue_count = (instance.get("rcsb_polymer_instance_info") or {}).get("modeled_residue_count")

        pdbx_mutation = (instance.get("polymer_entity") or {}) \
                            .get("rcsb_polymer_entity", {}) \
                            .get("pdbx_mutation")

        rcsb_mutation_count = (instance.get("polymer_entity") or {}) \
                                  .get("entity_poly", {}) \
                                  .get("rcsb_mutation_count")

        out[inst_id] = {
            "biological_assembly": list(bas_ids) if isinstance(bas_ids, (list, tuple, set)) else ([] if bas_ids is None else [bas_ids]),
            "missing_segments": missing_segments,        # list of {"entity_beg","entity_end"}
            "mapped_segments": mapped_segments,          # list of {"entity_range":{}, "uniprot_ranges":[{},...]}
            "unobs_res_cov": unobs_res_cov,
            "modeled_residue_count": modeled_residue_count,
            "pdbx_mutation": pdbx_mutation,
            "rcsb_mutation_count": rcsb_mutation_count,
        }

    return out

def fetchLigands(pdblist: List[str]):
    """
    For each PDB entry in `pdblist`, return ligands present and aggregated Binding Affinity data.

    Output:
    {
      "2JLE": [
        {
          "comp_id": "I15",
          "display_name": "I15",     # falls back to comp_id if no name/description
          "binding_affinity": {
            "IC50": {"unit": "nM", "min": 50.0, "max": 384.0, "count": 4},
            "Ki":   {"unit": "nM", "min": 12.0, "max": 20.0,  "count": 2},
            ...
          },
          "provenance_codes": ["BindingDB"],  # unique sources seen for this ligand
        },
        ...
      ],
      "XXXX": None
    }
    """
    if not pdblist:
        return {}

    query = Query(
        input_type="entries",
        input_ids=pdblist,
        return_data_list=[
            # Entry-level binding affinity “table”
            "rcsb_binding_affinity.comp_id",
            "rcsb_binding_affinity.type",
            "rcsb_binding_affinity.value",
            "rcsb_binding_affinity.unit",
            "rcsb_binding_affinity.symbol",
            "rcsb_binding_affinity.reference_sequence_identity",
            "rcsb_binding_affinity.provenance_code",

            # Non-polymer *entities* for nicer display
            "nonpolymer_entities.pdbx_entity_nonpoly.comp_id",
            "nonpolymer_entities.pdbx_entity_nonpoly.name",
            "nonpolymer_entities.rcsb_nonpolymer_entity.pdbx_description",
            "nonpolymer_entities.rcsb_nonpolymer_entity.formula_weight",
        ]
    )
    resp = query.exec()
    
    out = {}
    for entry in (resp.get("data") or {}).get("entries") or []:
        pdbid = entry.get("rcsb_id")
        if not pdbid:
            continue

        # 1) Index all non-polymer entities (ligands) present in the entry
        #    → comp_id -> basic metadata
        comp_meta = {}
        for e in entry.get("nonpolymer_entities") or []:
            en = e.get("pdbx_entity_nonpoly") or {}
            rn = e.get("rcsb_nonpolymer_entity") or {}
            comp_id = en.get("comp_id")
            if not comp_id:
                continue
            comp_meta[comp_id] = {
                "comp_id": comp_id,
                "name": en.get("name"),
                "description": rn.get("pdbx_description"),
                "formula_weight": rn.get("formula_weight"),
                # A simple display name fallback:
                "display_name": en.get("name") or rn.get("pdbx_description") or comp_id,
            }

        # 2) Prepare output map per entry: comp_id -> record (so we can attach affinities if any)
        comp_map = {cid: {**meta, "binding_affinity": {}, "provenance_codes": set()}
                    for cid, meta in comp_meta.items()}

        # 3) If the entry has binding-affinity rows, aggregate by comp_id and type
        #    Example fields: type (IC50/Ki/…), value, unit, provenance_code
        for r in entry.get("rcsb_binding_affinity") or []:
            cid   = r.get("comp_id")
            btype = r.get("type")
            val   = r.get("value")
            unit  = r.get("unit")
            prov  = r.get("provenance_code")

            # Skip malformed rows
            if not cid or btype is None or val is None:
                continue

            # If a ligand shows up only in affinity table (rare), seed minimal record
            if cid not in comp_map:
                comp_map[cid] = {
                    "comp_id": cid,
                    "name": None,
                    "description": None,
                    "formula_weight": None,
                    "display_name": cid,
                    "binding_affinity": {},
                    "provenance_codes": set(),
                }

            # Aggregate min/max/count per type
            slot = comp_map[cid]["binding_affinity"].setdefault(
                btype, {"unit": unit, "min": val, "max": val, "count": 0}
            )
            slot["unit"] = slot["unit"] or unit
            slot["count"] += 1
            slot["min"] = min(slot["min"], val)
            slot["max"] = max(slot["max"], val)

            if prov:
                comp_map[cid]["provenance_codes"].add(prov)

        # 4) Finalize JSON-friendly list for this PDB id
        items = []
        for rec in comp_map.values():
            rec["provenance_codes"] = sorted(rec["provenance_codes"])
            items.append(rec)

        # If there were no ligands at all, store None
        out[pdbid] = items or None

    return out

def fetchOligosaccharides(pdblist: List[str]):
    """
    For each PDB entry in `pdblist`, return a list of branched (oligosaccharide/glycan) entities.

    Output schema:
    {
      "XXXX": [
        {
          "branched_entity_id": "7ABC_5",      # entity id
          "type": "oligosaccharide",
          "description": "alpha-D-glucopyranose-(1-6)-beta-D-glucopyranose",
          "formula_weight_kDa": 0.745,
          "descriptors": [
              {"type": "LINUCS", "descriptor": "[][a-D-Manp]{...}"},
              {"type": "Glycam", "descriptor": "DManpb1-4DGlcpNAc..."},
              {"type": "WURCS",  "descriptor": "WURCS=..."}
          ]
        },
        ...
      ],
      "YYYY": None
    }

    Attributes used are under branched_entities (Carbohydrates).
    """
    query = Query(
        input_type="entries",
        input_ids=pdblist,
        return_data_list=[
            "branched_entities.rcsb_id",
            "branched_entities.pdbx_entity_branch.type",
            "branched_entities.rcsb_branched_entity.pdbx_description",
            "branched_entities.rcsb_branched_entity.formula_weight",
            "branched_entities.pdbx_entity_branch_descriptor.type",
            "branched_entities.pdbx_entity_branch_descriptor.descriptor",
        ],
    )
    resp = query.exec()

    out = {}
    for entry in resp.get("data", {}).get("entries", []):
        pdbid = entry.get("rcsb_id")
        bes = entry.get("branched_entities")
        if not bes:
            out[pdbid] = None
            continue

        items = []
        for b in bes:
            be_id = b.get("rcsb_id")
            btype = (b.get("pdbx_entity_branch") or {}).get("type")
            desc = (b.get("rcsb_branched_entity") or {}).get("pdbx_description")
            fw = (b.get("rcsb_branched_entity") or {}).get("formula_weight")

            descriptors = []
            for d in (b.get("pdbx_entity_branch_descriptor") or []):
                dtype = d.get("type")
                dval = d.get("descriptor")
                if dtype and dval:
                    descriptors.append({"type": dtype, "descriptor": dval})

            items.append({
                "branched_entity_id": be_id,
                "type": btype,
                "description": desc,
                "formula_weight_kDa": fw,
                "descriptors": descriptors,
            })

        out[pdbid] = items or None

    return out

def fetchMetadata(pdblist: List[str]) -> Dict[str, Dict[str, Any]]:
    """
    Fetch per-entry metadata, polymer entities, title/DOI, and
    symmetry/stoichiometry + unique protein chains using the RCSB Data API.

    Adds:
      - title (struct.title)
      - pdb_doi (database_2.pdbx_DOI)
      - primary_citation_doi (rcsb_primary_citation.pdbx_database_id_DOI)
      - unique_protein_chains (rcsb_entry_info.polymer_entity_count_protein)
      - assemblies: list of {
            assembly_id,
            protein_chain_instances,       # rcsb_assembly_info.polymer_entity_instance_count_protein
            global_symmetry: {type, symbol, stoichiometry} | None,
            pseudo_symmetry: {type, symbol, stoichiometry} | None
        }
    """
    if not pdblist:
        return {}

    q = Query(
        input_type="entries",
        input_ids=pdblist,
        return_data_list=[
            # entry id
            "entries.rcsb_id",

            # title & DOIs
            "struct.title",
            "database_2.pdbx_DOI",
            "rcsb_primary_citation.pdbx_database_id_DOI",

            # entry-level metadata
            "exptl.method",
            "rcsb_entry_info.resolution_combined",
            "em_3d_reconstruction.resolution",
            "pdbx_vrpt_summary_em.Q_score",
            "pdbx_vrpt_summary_diffraction.Q_score",
            "rcsb_accession_info.initial_release_date",
            "refine.ls_R_factor_R_free",
            "refine.ls_R_factor_R_work",

            # NEW: unique protein chains (distinct protein entities)
            "rcsb_entry_info.polymer_entity_count_protein",

            # NEW: per-assembly symmetry & protein chain instances
            "assemblies.rcsb_assembly_info.assembly_id",
            "assemblies.rcsb_assembly_info.polymer_entity_instance_count_protein",
            "assemblies.rcsb_struct_symmetry.kind",
            "assemblies.rcsb_struct_symmetry.type",
            "assemblies.rcsb_struct_symmetry.symbol",
            "assemblies.rcsb_struct_symmetry.stoichiometry",

            # polymer entity identifiers (entity + chains)
            "polymer_entities.rcsb_polymer_entity_container_identifiers.entity_id",
            "polymer_entities.rcsb_polymer_entity_container_identifiers.asym_ids",
            "polymer_entities.rcsb_polymer_entity_container_identifiers.auth_asym_ids",

            # names, UniProt
            "polymer_entities.uniprots.rcsb_uniprot_protein.name.value",
            "polymer_entities.uniprots.rcsb_uniprot_container_identifiers.uniprot_id",
            "polymer_entities.rcsb_polymer_entity.pdbx_description",

            # organism
            "polymer_entities.rcsb_entity_source_organism.scientific_name",
            "polymer_entities.rcsb_entity_source_organism.ncbi_taxonomy_id",

            # polymer type + length
            "polymer_entities.entity_poly.rcsb_entity_polymer_type",
            "polymer_entities.entity_poly.rcsb_sample_sequence_length",
        ]
    )

    resp = q.exec()
    entries = (resp.get("data") or {}).get("entries") or []
    out: Dict[str, Dict[str, Any]] = {}

    for entry in entries:
        pdbid = entry.get("rcsb_id")
        if not pdbid:
            continue

        # --- title & DOIs ---
        title = (entry.get("struct") or {}).get("title")
        pdb_doi = None
        for db2 in entry.get("database_2") or []:
            if db2.get("pdbx_DOI"):
                pdb_doi = db2["pdbx_DOI"]
                break
        primary_citation_doi = (entry.get("rcsb_primary_citation") or {}).get("pdbx_database_id_DOI")

        # --- entry-level metadata ---
        method = entry.get("exptl", [{}])[0].get("method") if entry.get("exptl") else None
        release_date = (entry.get("rcsb_accession_info") or {}).get("initial_release_date")

        resolution = None
        rc = (entry.get("rcsb_entry_info") or {}).get("resolution_combined")
        if isinstance(rc, list) and rc:
            resolution = rc[0]
        elif isinstance(rc, (float, int)):
            resolution = rc

        em_resolution = (entry.get("em_3d_reconstruction", [{}]) or [{}])[0].get("resolution") \
                        if entry.get("em_3d_reconstruction") else None

        q_score = None
        em_q = entry.get("pdbx_vrpt_summary_em")
        if isinstance(em_q, list) and em_q:
            q_score = em_q[0].get("Q_score")
        if q_score is None:
            diff_q = entry.get("pdbx_vrpt_summary_diffraction")
            if isinstance(diff_q, list) and diff_q:
                q_score = diff_q[0].get("Q_score")

        r_work = r_free = None
        ref = entry.get("refine")
        if isinstance(ref, list) and ref:
            r_work = ref[0].get("ls_R_factor_R_work")
            r_free = ref[0].get("ls_R_factor_R_free")

        # --- NEW: unique protein chains ---
        unique_protein_chains = (entry.get("rcsb_entry_info") or {}).get("polymer_entity_count_protein")

        # --- NEW: per-assembly symmetry & protein instances ---
        assemblies_out: List[Dict[str, Any]] = []
        for asm in entry.get("assemblies") or []:
            asm_info = asm.get("rcsb_assembly_info") or {}
            assembly_id = asm_info.get("assembly_id")
            prot_inst = asm_info.get("polymer_entity_instance_count_protein")

            global_sym, pseudo_sym = None, None
            for sym in asm.get("rcsb_struct_symmetry") or []:
                payload = {
                    "type": sym.get("type"),
                    "symbol": sym.get("symbol"),
                    "stoichiometry": sym.get("stoichiometry"),
                }
                if sym.get("kind") == "Global Symmetry" and global_sym is None:
                    global_sym = payload
                elif sym.get("kind") == "Pseudo Symmetry" and pseudo_sym is None:
                    pseudo_sym = payload

            assemblies_out.append({
                "assembly_id": assembly_id,
                "protein_chain_instances": prot_inst,
                "global_symmetry": global_sym,
                "pseudo_symmetry": pseudo_sym,
            })

        # --- polymer entities (unchanged logic) ---
        entities_out: List[Dict[str, Any]] = []
        for pe in entry.get("polymer_entities", []) or []:
            ids = pe.get("rcsb_polymer_entity_container_identifiers") or {}
            entity_id = ids.get("entity_id")
            entity_rcsb_id = f"{pdbid}_{entity_id}" if entity_id is not None else None
            label_asym_ids = ids.get("asym_ids") or []
            auth_asym_ids  = ids.get("auth_asym_ids") or []

            uniprots = pe.get("uniprots") or []
            up_name = None
            up_ids: List[str] = []
            if uniprots:
                up_name = (uniprots[0].get("rcsb_uniprot_protein") or {}).get("name", {}).get("value")
                for u in uniprots:
                    uid = (u.get("rcsb_uniprot_container_identifiers") or {}).get("uniprot_id")
                    if uid:
                        up_ids.append(uid)

            description = (pe.get("rcsb_polymer_entity") or {}).get("pdbx_description")
            name = up_name or description

            orgs = pe.get("rcsb_entity_source_organism") or []
            organism_names = [o.get("scientific_name") for o in orgs if o and o.get("scientific_name")]
            taxonomy_ids   = [o.get("ncbi_taxonomy_id") for o in orgs if o and (o.get("ncbi_taxonomy_id") is not None)]

            poly = pe.get("entity_poly") or {}
            polymer_type = poly.get("rcsb_entity_polymer_type")
            sample_len   = poly.get("rcsb_sample_sequence_length")

            entities_out.append({
                "entity_rcsb_id": entity_rcsb_id,
                "entity_id": entity_id,
                "label_asym_ids": label_asym_ids,
                "auth_asym_ids": auth_asym_ids,
                "name": name,
                "description": description,
                "polymer_type": polymer_type,
                "organism_names": organism_names,
                "taxonomy_ids": taxonomy_ids,
                "uniprot_ids": up_ids,
                "sample_sequence_length": sample_len,
            })

        out[pdbid] = {
            "title": title,
            "pdb_doi": pdb_doi,
            "primary_citation_doi": primary_citation_doi,
            "method": method,
            "resolution": resolution,
            "em_resolution": em_resolution,
            "q_score": q_score,
            "r_work": r_work,
            "r_free": r_free,
            "release_date": release_date,
            "unique_protein_chains": unique_protein_chains,     # NEW
            "assemblies": assemblies_out,                       # NEW
            "polymer_entities": entities_out,
        }

    return out

def queryUid2RCSB(uid):
    """Query UniProtID to collect all PDB ID (entities and instances)"""
    # uniprot_id = 'P0DMS8'
    q_acc = AttributeQuery(
        attribute='rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession',
        value=uid,
        operator="exact_match",
    )
    q_db = AttributeQuery(
        attribute='rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_name',
        value="UniProt",
        operator="exact_match",
    )
    
    # Group nested attributes using `NestedAttributeQuery`
    query = NestedAttributeQuery(q_acc, q_db)
    # Query data
    pdb_id = list(query())
    pdb_entity = list(query(return_type='polymer_entity'))
    pdb_instance = list(query(return_type='polymer_instance'))

    # Retrieve
    out = {}
    for id in pdb_id:
        _entity = next(
            (_ent for _ent in pdb_entity if _ent.startswith(f"{id}_")), None
        )
        if not _entity:
            continue
        
        _instance = [_ins for _ins in pdb_instance if _ins.startswith(f"{id}.")]
        sample = {}
        # sample["pdb_id"] = _entity[:4]
        sample["pdb_entity"] = _entity
        sample["pdb_instance"] = _instance
        out[_entity[:4]] = sample
    return out

def queryDrug2RCSB(dbid: str):
    q_chem = AttributeQuery(
        attribute="rcsb_chem_comp_container_identifiers.drugbank_id",
        operator="exact_match",
        value=dbid,
    )
    ligand_id = list(q_chem(return_type="mol_definition"))[0]
    pdblist = list(q_chem())

    return {
        'id': dbid,
        'drug_ligand_id': ligand_id,
        'pdbid_with_drug_ligand_id': pdblist
    }

def align_RCSB2UniProt(pdb_entity, uid):
    """
    Align between P05106 and 7TD8
    [{'target_end': 497,
      'target_begin': 27,
      'query_end': 471,
      'query_begin': 1,
      'exon_shift': None,
      'difference': []}]

    target: uniprot sequence
    query: pdb sequence 
    """
    # Fetch alignments between a UniProt Accession and PDB Entity 
    # (i.e., unique sequence within the entry)
    query = Alignments(
        db_from="PDB_ENTITY",
        db_to="UNIPROT",
        query_id=pdb_entity,
        return_data_list=["query_sequence", "target_alignments"]
    )
    r = query.exec()
    
    uid_record = next(
        (item for item in r['data']['alignments']['target_alignments'] \
        if item['target_id'] == uid), None
    )
    if not uid_record:
        LOGGER.warn(f"No information for {pdb_entity}")
        return None
    aligned_regions = uid_record['aligned_regions']
    query_seq = r['data']['alignments']['query_sequence']
    target_seq = uid_record['target_sequence']

    for i, region in enumerate(aligned_regions):
        pdb_seq = query_seq[region['query_begin']-1 : region['query_end']]
        uniprot_seq = target_seq[region['target_begin']-1 : region['target_end']]

        # Find residues that disagree between PDB and UniProt 
        difference = []
        for j, (pdb_aa, uniprot_aa) in enumerate(zip(pdb_seq, uniprot_seq)):
            if pdb_aa != uniprot_aa:
                difference.append({
                    'pdb_resID': region['query_begin']+j,
                    'uniprot_resID': region['target_begin']+j,
                    'uniprot_aa': uniprot_aa,
                    'pdb_aa': pdb_aa,
                })
        aligned_regions[i]['difference'] = difference
    return {
        'aligned_regions': aligned_regions,
        'query_seq': query_seq,
    }

def ChEBI2ligandID(ChEBI):
    # Using ChEBI
    q1 = AttributeQuery(
        attribute="rcsb_chem_comp_related.resource_name",
        operator="exact_match",
        value="ChEBI"  # can also use "ChEMBL", "DrugBank", or "PubChem"
    )
    q2 = AttributeQuery(
        attribute="rcsb_chem_comp_related.resource_accession_code",
        operator="exact_match",
        value=ChEBI,
    )
    q2 = NestedAttributeQuery(q1, q2)
    r = list(q2(return_type="mol_definition"))
    return r[0]

def findDrugBindingSite(pdbid, ligand_list, cutoff=5, folder='.'):
    """ligandid for drug"""
    
    pdb = fetchPDB(pdbid, folder=folder, format='cif')
    pdb = parseMMCIF(pdb, resnums_mode='label_seq_id')
    protein = pdb.select('protein').copy()
    inhibitor_sel = ""
    for i, ligandid in enumerate(ligand_list):
        if i == len(ligand_list)-1:
            inhibitor_sel += f"resname {str(ligandid)}" 
        else:
            inhibitor_sel += f"resname {str(ligandid)} or " 
    inhibitor = pdb.select(inhibitor_sel)

    if not inhibitor:
        LOGGER.warn(f"Cannot detect {ligand_list} in {pdbid}")
        return {}

    contacts_ca = protein.select(f'calpha and (same residue as within {cutoff} of inhibitor)', inhibitor=inhibitor)

    chids   = contacts_ca.getSegnames() # follow label_asym_ids
    resnums = contacts_ca.getResnums() # follow label_seq_id
    resnames= contacts_ca.getResnames()

    # unique (chid, resnum, resname) in order
    triples = list(dict.fromkeys(zip(chids, resnums, resnames)))
    by_chain = defaultdict(list)
    for chid, resnum, resname in triples:
        by_chain[chid].append((int(resnum), resname))   # e.g. (91, 'GLY')
    
    return by_chain