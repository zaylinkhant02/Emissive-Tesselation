import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

def create_emissive_octagon_square_tessellation(cols=30, rows=30, side_length=1.0, gradient_type='radial', cmap_name='plasma'):
    W = side_length * (1.0 + np.sqrt(2))
    
    max_x = cols * W
    max_y = rows * W
    center_x = max_x / 2
    center_y = max_y / 2
    max_dist = np.sqrt(center_x**2 + center_y**2)
    
    bg_color = '#0b0c10' 
    bg_rgb = np.array([11/255, 12/255, 16/255])
    
    fig, ax = plt.subplots(figsize=(12, 12), facecolor=bg_color)
    ax.set_facecolor(bg_color)
    ax.set_aspect('equal')
    
    cmap = plt.colormaps[cmap_name]
    
    scale_shadow = 0.97
    scale_main   = 0.92
    scale_core   = 0.58
    
    shadow_offset = np.array([0.0, -W * 0.03])
    
    for r in range(-1, rows + 1):
        cy = r * W
        for c in range(-1, cols + 1):
            cx = c * W
            
            cell_shapes = []
            
            s2 = side_length / 2
            w2 = W / 2
            
            oct_verts = np.array([
                [cx + s2, cy + w2],
                [cx - s2, cy + w2],
                [cx - w2, cy + s2],
                [cx - w2, cy - s2],
                [cx - s2, cy - w2],
                [cx + s2, cy - w2],
                [cx + w2, cy - s2],
                [cx + w2, cy + s2]
            ])
            oct_center = np.array([cx, cy])
            cell_shapes.append((oct_verts, oct_center, 0))
            
            sq_verts = np.array([
                [cx + w2,           cy + s2],
                [cx + W - s2,       cy + w2],
                [cx + w2,           cy + W - s2],
                [cx + s2,           cy + w2]
            ])
            sq_center = np.array([cx + w2, cy + w2])
            cell_shapes.append((sq_verts, sq_center, 1))
            
            for vertices, center_point, shape_type in cell_shapes:
                cx_shape, cy_shape = center_point[0], center_point[1]
                
                if cx_shape < -W or cx_shape > max_x + W or cy_shape < -W or cy_shape > max_y + W:
                    continue
                
                if gradient_type == 'linear_x':
                    v = cx_shape / max_x
                elif gradient_type == 'linear_y':
                    v = cy_shape / max_y
                elif gradient_type == 'radial':
                    dist = np.sqrt((cx_shape - center_x)**2 + (cy_shape - center_y)**2)
                    v = 1.0 - (dist / max_dist)
                else:
                    v = 0.5
                
                v = np.clip(v, 0.0, 1.0)
                base_color = np.array(cmap(v)[:3])
                
                face_type = (r + 2 * c + shape_type) % 3
                
                if face_type == 0:
                    face_color = base_color + (1.0 - base_color) * 0.22
                elif face_type == 1:
                    face_color = base_color * 0.90
                else:
                    face_color = base_color * 0.50 + bg_rgb * 0.50
                
                verts_shadow = center_point + scale_shadow * (vertices - center_point) + shadow_offset
                shadow_patch = Polygon(
                    verts_shadow,
                    closed=True,
                    facecolor='#020205',
                    edgecolor='none',
                    alpha=0.42,
                    zorder=1
                )
                ax.add_patch(shadow_patch)
                
                verts_main = center_point + scale_main * (vertices - center_point)
                main_patch = Polygon(
                    verts_main,
                    closed=True,
                    facecolor=face_color,
                    edgecolor='none',
                    alpha=0.85,
                    zorder=2
                )
                ax.add_patch(main_patch)
                
                core_color = base_color + (1.0 - base_color) * 0.35
                verts_core = center_point + scale_core * (vertices - center_point)
                core_patch = Polygon(
                    verts_core,
                    closed=True,
                    facecolor=core_color,
                    edgecolor='none',
                    alpha=0.95,
                    zorder=3
                )
                ax.add_patch(core_patch)
                
    ax.set_xlim(0, max_x)
    ax.set_ylim(0, max_y)
    ax.axis('off')
    
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
    plt.show()

create_emissive_octagon_square_tessellation(cols=25, rows=25, side_length=1.0, gradient_type='radial', cmap_name='plasma')
