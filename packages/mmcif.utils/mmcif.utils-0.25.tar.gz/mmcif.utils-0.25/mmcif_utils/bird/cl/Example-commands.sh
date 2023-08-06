#!/bin/sh
#
export CVS_REPOSITORY_PATH="/cvs-ligands"
export CVS_REPOSITORY_HOST="HOSTNAME"
export CVS_REPOSITORY_USER="USER"
export CVS_REPOSITORY_PASSWORD="PASSWORD"        

python PdbxPrdExec.py --help
#
#  Create PRD id code lists from repository files -
#
python PdbxPrdExec.py --list_id_codes=REL  -o prd_released_ids.list \
		    --cvs_path /data/components/prd-v3
python PdbxPrdExec.py --list_id_codes=HOLD -o prd_hold_ids.list \
		    --cvs_path /data/components/prd-v3
python PdbxPrdExec.py --list_id_codes=ALL  -o prd_all_ids.list \
		    --cvs_path /data/components/prd-v3
#
# Export concatenated/split files from PRD id lists -- 
#
python PdbxPrdExec.py -v -i prd_all_ids.list \
			-o prd-all.cif \
			--export_from_list  \
			--cvs_path /data/components/prd-v3
#
python PdbxPrdExec.py -v  -i prd_released_ids.list \
			-o prd-rel.cif \
			--export_from_list \
                         --suppress_chem_comp_file="REF_ONLY_CC.list" \
			--strip_internal_items \
			--export_release_date='2012-12-12' \
			--cvs_path /data/components/prd-v3

#
python PdbxPrdExec.py  -v -i prd_released_ids.list \
			-o prd-rel.tar.gz \
			--export_from_list \
                         --suppress_chem_comp_file="REF_ONLY_CC.list" \
			--export_release_date='2012-12-12' \
			--strip_internal_items \
			--cvs_path /data/components/prd-v3
#
# Export repository files by status code -  (Typical update command)
#
python PdbxPrdExec.py  -v -o prd-rel-2.cif \
			--export_public_file \
                         --suppress_chem_comp_file="REF_ONLY_CC.list" \
			--strip_internal_items \
			--cvs_path /data/components/prd-v3
#
python PdbxPrdExec.py  -v -o prd-rel-2.tar.gz \
			--export_public_targzfile \
                         --suppress_chem_comp_file="REF_ONLY_CC.list" \
			--strip_internal_items \
			--cvs_path /data/components/prd-v3
#
# Export PRDCC repository files by status code -  (Typical update command)
#
python PdbxPrdExec.py  -v -o prdcc-rel.cif \
			--export_public_prdcc_file \
			--cvs_path /data/components/prd-v3 \
			--cvs_prdcc_path /data/components/prdcc-v3
#
python PdbxPrdExec.py  -v -o prdcc-rel.tar.gz \
			--export_public_prdcc_targzfile \
			--cvs_path /data/components/prd-v3 \
			--cvs_prdcc_path /data/components/prdcc-v3
#
#
python PdbxPrdExec.py -v --list_chem_comp_id_codes  -o cc_referenced_ids.list \
		    --cvs_path /data/components/test-project-v1
#
python PdbxPrdExec.py -v --cvs_checkout --cvs_path /data/components/test-project-v1
#
python PdbxPrdExec.py -v --set_cvs_release_status   --prd_id PRD_000001 \
		    --cvs_path /data/components/test-project-v1
