# Synopsis:
#
# ./demo/cdo_regrid.sh $PWD/.gribmagic-data/icon_global_icosahedral_model-level_2021080612_078_90_T.grib2 $PWD/icon_global_regular-lat-lon_model-level_2021080612_078_90_T.grib2
#

function regrid_ecmwf() {

    # https://confluence.ecmwf.int/display/CKB/How+to+plot+GRIB+files+with+Python+and+matplotlib

    # Generate weights.
    cdo -s gencon,grid.R720x360.txt frp_01.grb remapweights.rencon.R3600x1800.to.R720x360.grb

    # Apply regridding.
    cdo -s remap,grid.R720x360.txt,remapweights.rencon.R3600x1800.to.R720x360.grb frp_01.grb frp_05.grb

}

function regrid_dwd() {

    in_file=$1
    out_file=$2

    # https://www.dwd.de/DE/leistungen/opendata/help/modelle/Opendata_cdo_DE.pdf?__blob=publicationFile
    # https://opendata.dwd.de/weather/lib/cdo/

    # Configure grib type
    REGRID_INFO=ICON_GLOBAL2WORLD_025_EASY
    TARGET_GRID_DESCRIPTION=./${REGRID_INFO}/target_grid_world_025.txt
    WEIGHTS_FILE=./${REGRID_INFO}/weights_icogl2world_025.nc

    # Enter workspace
    mkdir -p /tmp/regrid
    cd /tmp/regrid

    # Acquire grid description files
    wget --no-clobber https://opendata.dwd.de/weather/lib/cdo/${REGRID_INFO}.tar.bz2
    test ! -d ${REGRID_INFO} && tar -xjf ${REGRID_INFO}.tar.bz2

    # Apply regridding.
    cdo --format=grb2 remap,${TARGET_GRID_DESCRIPTION},${WEIGHTS_FILE} ${in_file} ${out_file}

    # Leave workspace
    cd -

}

regrid_dwd $1 $2
