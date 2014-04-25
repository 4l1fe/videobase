from subprocess import PIPE, Popen
import json




def render_page(page_type,context):
        render_proc = Popen(['nodejs', 'renderproc.js'], stdin=PIPE, stdout=PIPE)
        html,status = render_proc.communicate(json.dumps({
            "template": page_type,
            "context": context
        }))

        return html






