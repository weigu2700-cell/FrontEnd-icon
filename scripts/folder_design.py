"""Folder keylines and aspect-preserving motif layout on a shared 24px canvas."""
import colorsys

# Every directory keeps this tab and outer silhouette. Motifs never cover the tab.
FOLDER_PATH = 'M1.5 5.5a2 2 0 0 1 2-2H8.6c.6 0 1.1.2 1.5.6l2 1.9h8.4a2 2 0 0 1 2 2v10.5a2 2 0 0 1-2 2h-17a2 2 0 0 1-2-2Z'
OPEN_FRONT = 'M4 8.5h17.2c.9 0 1.5.8 1.2 1.6l-2.2 8.9c-.2.9-1 1.5-1.9 1.5H3.5c-1.3 0-2.2-1.1-1.9-2.3l1.3-8.1c.1-.9.6-1.6 1.1-1.6Z'

def palette(color):
    r,g,b=(int(color[i:i+2],16)/255 for i in (1,3,5))
    h,_,_=colorsys.rgb_to_hls(r,g,b)
    def tone(light,saturation):
        return '#'+''.join(f'{round(c*255):02X}' for c in colorsys.hls_to_rgb(h,light,saturation))
    return tone(.49,.68),tone(.86,.80),tone(.38,.63)

def render_folder(name, color, art=None, opened=False, style='foreground'):
    base,motive,rear=palette(art['color'] if art else color)
    body=f'<path data-role="folder-shell" d="{FOLDER_PATH}" fill="{rear}"/>'
    if opened:
        body+=f'<path data-role="folder-front" d="{OPEN_FRONT}" fill="{base}"/>'
    else:
        body+=f'<path data-role="folder-front" d="M1.5 8h19a2 2 0 0 1 2 2v8.5a2 2 0 0 1-2 2h-17a2 2 0 0 1-2-2Z" fill="{base}"/>'
    if art:
        # Fit real ink bounds, never stretch the source into a fixed rectangle.
        x,y,width,height=art['bounds']
        if style in ('foreground','layered'):
            scale=min(16/width,15.5/height)
            tx=22.5-(x+width)*scale
            ty=22.5-(y+height)*scale
        elif style=='inset':
            scale=min(14.5/width,12.5/height)
            tx=12.25-(x+width/2)*scale
            ty=13.5-(y+height/2)*scale
        else:
            raise ValueError(style)
        body+=f'<g data-role="business-motif" transform="translate({tx:.6f} {ty:.6f}) scale({scale:.8f})">'
        body+=''.join(f'<path d="{d}" fill="{motive}"/>' for d in art['paths'])+'</g>'
    return body
