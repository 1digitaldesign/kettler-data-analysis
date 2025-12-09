#!/usr/bin/env python3
"""
GIS File Converter using GDAL
Converts between various geospatial formats (Shapefile, GeoJSON, KML, etc.)
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional, Any
import json
from datetime import datetime

try:
    from osgeo import gdal, ogr, osr
    GDAL_AVAILABLE = True
except ImportError:
    GDAL_AVAILABLE = False
    print("Warning: GDAL not available. Install with: pip install gdal")

try:
    import geopandas as gpd
    GEOPANDAS_AVAILABLE = True
except ImportError:
    GEOPANDAS_AVAILABLE = False
    print("Warning: GeoPandas not available. Install with: pip install geopandas")

try:
    import fiona
    FIONA_AVAILABLE = True
except ImportError:
    FIONA_AVAILABLE = False
    print("Warning: Fiona not available. Install with: pip install fiona")

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts.utils.paths import DATA_DIR, DATA_SCRAPED_DIR


class GISConverter:
    """Convert GIS files between formats using GDAL"""

    SUPPORTED_FORMATS = {
        'shp': 'ESRI Shapefile',
        'geojson': 'GeoJSON',
        'kml': 'KML',
        'kmz': 'KML',
        'gpkg': 'GPKG',
        'gml': 'GML',
        'geotiff': 'GTiff',
        'tif': 'GTiff',
        'tiff': 'GTiff',
    }

    def __init__(self):
        if not GDAL_AVAILABLE:
            raise ImportError("GDAL is required. Install with: pip install gdal")

        # Enable GDAL exceptions
        gdal.UseExceptions()
        ogr.UseExceptions()

    def detect_format(self, file_path: Path) -> Optional[str]:
        """Detect GIS file format from extension"""
        ext = file_path.suffix.lower().lstrip('.')
        return self.SUPPORTED_FORMATS.get(ext)

    def get_driver_name(self, output_format: str) -> str:
        """Get GDAL driver name for format"""
        format_map = {
            'shp': 'ESRI Shapefile',
            'geojson': 'GeoJSON',
            'kml': 'KML',
            'kmz': 'KML',
            'gpkg': 'GPKG',
            'gml': 'GML',
            'geotiff': 'GTiff',
            'tif': 'GTiff',
            'tiff': 'GTiff',
        }
        return format_map.get(output_format.lower(), output_format)

    def convert_file(self, input_path: Path, output_path: Path,
                     output_format: str = 'geojson',
                     target_srs: Optional[str] = None) -> Dict[str, Any]:
        """
        Convert GIS file from one format to another

        Args:
            input_path: Input file path
            output_path: Output file path
            output_format: Output format (geojson, shp, kml, etc.)
            target_srs: Target spatial reference system (EPSG code, e.g., 'EPSG:4326')

        Returns:
            Dictionary with conversion metadata
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Detect input format
        input_format = self.detect_format(input_path)
        if not input_format:
            raise ValueError(f"Unsupported input format: {input_path.suffix}")

        # Get output driver
        output_driver_name = self.get_driver_name(output_format)
        output_driver = ogr.GetDriverByName(output_driver_name)
        if output_driver is None:
            raise ValueError(f"Unsupported output format: {output_format}")

        # Open input dataset
        input_ds = ogr.Open(str(input_path))
        if input_ds is None:
            raise ValueError(f"Could not open input file: {input_path}")

        try:
            # Get input layer
            input_layer = input_ds.GetLayer(0)
            if input_layer is None:
                raise ValueError("Input file has no layers")

            # Get input spatial reference
            input_srs = input_layer.GetSpatialRef()

            # Create output dataset
            if output_path.exists():
                output_driver.DeleteDataSource(str(output_path))

            output_ds = output_driver.CreateDataSource(str(output_path))
            if output_ds is None:
                raise ValueError(f"Could not create output file: {output_path}")

            # Set target SRS
            if target_srs:
                target_srs_obj = osr.SpatialReference()
                target_srs_obj.SetFromUserInput(target_srs)
            else:
                target_srs_obj = input_srs

            # Create output layer
            output_layer = output_ds.CreateLayer(
                output_path.stem,
                target_srs_obj,
                input_layer.GetGeomType()
            )

            # Copy field definitions
            input_layer_defn = input_layer.GetLayerDefn()
            for i in range(input_layer_defn.GetFieldCount()):
                field_defn = input_layer_defn.GetFieldDefn(i)
                output_layer.CreateField(field_defn)

            # Transform coordinates if needed
            if target_srs and input_srs and not input_srs.IsSame(target_srs_obj):
                transform = osr.CoordinateTransformation(input_srs, target_srs_obj)
            else:
                transform = None

            # Copy features
            feature_count = 0
            input_layer.ResetReading()

            for feature in input_layer:
                geom = feature.GetGeometryRef()
                if geom is not None:
                    if transform:
                        geom.Transform(transform)

                    output_feature = ogr.Feature(output_layer.GetLayerDefn())
                    output_feature.SetGeometry(geom)

                    # Copy attributes
                    for i in range(input_layer_defn.GetFieldCount()):
                        field_name = input_layer_defn.GetFieldDefn(i).GetName()
                        output_feature.SetField(field_name, feature.GetField(field_name))

                    output_layer.CreateFeature(output_feature)
                    output_feature = None
                    feature_count += 1

            output_ds = None

            return {
                'status': 'success',
                'input_file': str(input_path),
                'output_file': str(output_path),
                'input_format': input_format,
                'output_format': output_format,
                'feature_count': feature_count,
                'input_srs': input_srs.ExportToWkt() if input_srs else None,
                'output_srs': target_srs_obj.ExportToWkt() if target_srs_obj else None,
                'conversion_date': datetime.now().isoformat()
            }

        finally:
            input_ds = None

    def convert_to_geojson(self, input_path: Path, output_path: Optional[Path] = None,
                          target_srs: str = 'EPSG:4326') -> Dict[str, Any]:
        """Convert any GIS file to GeoJSON"""
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}.geojson"

        return self.convert_file(input_path, output_path, 'geojson', target_srs)

    def convert_to_shapefile(self, input_path: Path, output_path: Optional[Path] = None,
                            target_srs: Optional[str] = None) -> Dict[str, Any]:
        """Convert any GIS file to Shapefile"""
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}.shp"

        return self.convert_file(input_path, output_path, 'shp', target_srs)

    def convert_to_kml(self, input_path: Path, output_path: Optional[Path] = None,
                       target_srs: str = 'EPSG:4326') -> Dict[str, Any]:
        """Convert any GIS file to KML"""
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}.kml"

        return self.convert_file(input_path, output_path, 'kml', target_srs)

    def batch_convert(self, input_files: List[Path], output_format: str = 'geojson',
                     output_dir: Optional[Path] = None,
                     target_srs: Optional[str] = None) -> List[Dict[str, Any]]:
        """Convert multiple GIS files"""
        if output_dir is None:
            output_dir = DATA_DIR / "gis" / "converted"
        output_dir.mkdir(parents=True, exist_ok=True)

        results = []
        for input_file in input_files:
            try:
                output_file = output_dir / f"{input_file.stem}.{output_format}"
                result = self.convert_file(input_file, output_file, output_format, target_srs)
                results.append(result)
                print(f"Converted: {input_file.name} -> {output_file.name}")
            except Exception as e:
                results.append({
                    'status': 'error',
                    'input_file': str(input_file),
                    'error': str(e)
                })
                print(f"Error converting {input_file.name}: {e}")

        return results

    def extract_properties_from_geojson(self, geojson_path: Path) -> List[Dict[str, Any]]:
        """Extract property information from GeoJSON file"""
        with open(geojson_path, 'r') as f:
            geojson_data = json.load(f)

        properties = []

        if geojson_data.get('type') == 'FeatureCollection':
            features = geojson_data.get('features', [])
        elif geojson_data.get('type') == 'Feature':
            features = [geojson_data]
        else:
            return properties

        for feature in features:
            prop = feature.get('properties', {})
            geom = feature.get('geometry', {})

            # Extract geometry info
            prop['geometry_type'] = geom.get('type')
            prop['coordinates'] = geom.get('coordinates')

            properties.append(prop)

        return properties

    def merge_geojson_files(self, input_files: List[Path], output_path: Path) -> Dict[str, Any]:
        """Merge multiple GeoJSON files into one"""
        all_features = []

        for input_file in input_files:
            with open(input_file, 'r') as f:
                geojson_data = json.load(f)

            if geojson_data.get('type') == 'FeatureCollection':
                features = geojson_data.get('features', [])
            elif geojson_data.get('type') == 'Feature':
                features = [geojson_data]
            else:
                continue

            all_features.extend(features)

        merged_geojson = {
            'type': 'FeatureCollection',
            'features': all_features,
            'metadata': {
                'merged_date': datetime.now().isoformat(),
                'source_files': [str(f) for f in input_files],
                'feature_count': len(all_features)
            }
        }

        with open(output_path, 'w') as f:
            json.dump(merged_geojson, f, indent=2)

        return {
            'status': 'success',
            'output_file': str(output_path),
            'feature_count': len(all_features),
            'source_files': len(input_files)
        }

    def get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """Get information about a GIS file"""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Try using GDAL
        try:
            ds = ogr.Open(str(file_path))
            if ds is None:
                raise ValueError("Could not open file with GDAL")

            layer = ds.GetLayer(0)
            if layer is None:
                raise ValueError("File has no layers")

            srs = layer.GetSpatialRef()
            extent = layer.GetExtent()
            feature_count = layer.GetFeatureCount()

            info = {
                'file_path': str(file_path),
                'format': self.detect_format(file_path),
                'layer_count': ds.GetLayerCount(),
                'feature_count': feature_count,
                'geometry_type': ogr.GeometryTypeToName(layer.GetGeomType()),
                'srs': srs.ExportToWkt() if srs else None,
                'srs_epsg': srs.GetAuthorityCode(None) if srs else None,
                'extent': {
                    'min_x': extent[0],
                    'min_y': extent[2],
                    'max_x': extent[1],
                    'max_y': extent[3]
                },
                'fields': []
            }

            # Get field information
            layer_defn = layer.GetLayerDefn()
            for i in range(layer_defn.GetFieldCount()):
                field_defn = layer_defn.GetFieldDefn(i)
                info['fields'].append({
                    'name': field_defn.GetName(),
                    'type': field_defn.GetFieldTypeName(field_defn.GetType()),
                    'width': field_defn.GetWidth(),
                    'precision': field_defn.GetPrecision()
                })

            ds = None
            return info

        except Exception as e:
            # Fallback to GeoPandas if available
            if GEOPANDAS_AVAILABLE:
                try:
                    gdf = gpd.read_file(str(file_path))
                    return {
                        'file_path': str(file_path),
                        'format': self.detect_format(file_path),
                        'feature_count': len(gdf),
                        'geometry_type': str(gdf.geometry.type.iloc[0]) if len(gdf) > 0 else None,
                        'crs': str(gdf.crs) if gdf.crs else None,
                        'columns': list(gdf.columns),
                        'bounds': gdf.total_bounds.tolist() if len(gdf) > 0 else None
                    }
                except Exception as e2:
                    raise ValueError(f"Could not read file with GDAL or GeoPandas: {e}, {e2}")
            else:
                raise


if __name__ == "__main__":
    # Example usage
    if not GDAL_AVAILABLE:
        print("GDAL not available. Install with: pip install gdal")
        sys.exit(1)

    converter = GISConverter()

    # Example: Convert shapefile to GeoJSON
    # input_file = Path("data/gis/parcels.shp")
    # output_file = Path("data/gis/parcels.geojson")
    # result = converter.convert_to_geojson(input_file, output_file)
    # print(f"Conversion result: {result}")

    # Example: Get file info
    # info = converter.get_file_info(input_file)
    # print(f"File info: {info}")

    print("GIS Converter initialized successfully")
    print(f"Supported formats: {', '.join(converter.SUPPORTED_FORMATS.keys())}")
