import ezdxf
import math
from typing import Dict, List, Tuple
import logging

class CADProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Material-specific cutting parameters (mm/min)
        self.material_feed_rates = {
            'steel': 300,
            'aluminum': 600,
            'plastic': 800,
            'wood': 1200,
            'brass': 400,
            'copper': 350
        }
    
    def process_dxf(self, filepath: str) -> Dict:
        """
        Process DXF file and extract geometry information
        """
        try:
            doc = ezdxf.readfile(filepath)
            msp = doc.modelspace()
            
            geometry_data = {
                'total_length': 0.0,
                'line_count': 0,
                'arc_count': 0,
                'circle_count': 0,
                'polyline_count': 0,
                'entities': []
            }
            
            # Process different entity types
            for entity in msp:
                if entity.dxftype() == 'LINE':
                    length = self._calculate_line_length(entity)
                    geometry_data['total_length'] += length
                    geometry_data['line_count'] += 1
                    geometry_data['entities'].append({
                        'type': 'LINE',
                        'length': length,
                        'start': (entity.dxf.start.x, entity.dxf.start.y),
                        'end': (entity.dxf.end.x, entity.dxf.end.y)
                    })
                
                elif entity.dxftype() == 'ARC':
                    length = self._calculate_arc_length(entity)
                    geometry_data['total_length'] += length
                    geometry_data['arc_count'] += 1
                    geometry_data['entities'].append({
                        'type': 'ARC',
                        'length': length,
                        'center': (entity.dxf.center.x, entity.dxf.center.y),
                        'radius': entity.dxf.radius,
                        'start_angle': entity.dxf.start_angle,
                        'end_angle': entity.dxf.end_angle
                    })
                
                elif entity.dxftype() == 'CIRCLE':
                    length = self._calculate_circle_length(entity)
                    geometry_data['total_length'] += length
                    geometry_data['circle_count'] += 1
                    geometry_data['entities'].append({
                        'type': 'CIRCLE',
                        'length': length,
                        'center': (entity.dxf.center.x, entity.dxf.center.y),
                        'radius': entity.dxf.radius
                    })
                
                elif entity.dxftype() == 'LWPOLYLINE':
                    length = self._calculate_polyline_length(entity)
                    geometry_data['total_length'] += length
                    geometry_data['polyline_count'] += 1
                    geometry_data['entities'].append({
                        'type': 'LWPOLYLINE',
                        'length': length,
                        'points': list(entity.get_points())
                    })
                
                elif entity.dxftype() == 'POLYLINE':
                    length = self._calculate_polyline_length(entity)
                    geometry_data['total_length'] += length
                    geometry_data['polyline_count'] += 1
                    geometry_data['entities'].append({
                        'type': 'POLYLINE',
                        'length': length,
                        'points': list(entity.points)
                    })
            
            return geometry_data
            
        except Exception as e:
            self.logger.error(f"Error processing DXF file: {str(e)}")
            raise Exception(f"Failed to process DXF file: {str(e)}")
    
    def _calculate_line_length(self, line) -> float:
        """Calculate length of a line entity"""
        dx = line.dxf.end.x - line.dxf.start.x
        dy = line.dxf.end.y - line.dxf.start.y
        return math.sqrt(dx*dx + dy*dy)
    
    def _calculate_arc_length(self, arc) -> float:
        """Calculate arc length"""
        radius = arc.dxf.radius
        start_angle = math.radians(arc.dxf.start_angle)
        end_angle = math.radians(arc.dxf.end_angle)
        
        # Normalize angles
        if end_angle < start_angle:
            end_angle += 2 * math.pi
        
        angle_diff = end_angle - start_angle
        return radius * angle_diff
    
    def _calculate_circle_length(self, circle) -> float:
        """Calculate circle circumference"""
        return 2 * math.pi * circle.dxf.radius
    
    def _calculate_polyline_length(self, polyline) -> float:
        """Calculate polyline length"""
        total_length = 0.0
        points = list(polyline.get_points()) if hasattr(polyline, 'get_points') else list(polyline.points)
        
        for i in range(len(points) - 1):
            if len(points[i]) >= 2 and len(points[i+1]) >= 2:
                dx = points[i+1][0] - points[i][0]
                dy = points[i+1][1] - points[i][1]
                total_length += math.sqrt(dx*dx + dy*dy)
        
        return total_length
    
    def get_material_feed_rate(self, material: str) -> float:
        """Get feed rate for a specific material"""
        return self.material_feed_rates.get(material.lower(), 300)  # Default to steel rate
