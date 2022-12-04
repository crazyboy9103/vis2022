import glob, json
import streamlit.components.v1 as components
import glob
import json

full_comp_html = '''<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
'''
json_paths = glob.glob("./data/job_posting/json/*.json")
for idx, path in enumerate(json_paths[:100]):
  data = json.load(open(path, "r"))
  
  name = data["company_name"]
  thumb_img = data["title_thumb_img"]
  main_tasks = data["main_tasks"]
  is_newbie = data["is_newbie"]
  location = data["location"]
  req = data["requirements"]
  
  sub_categories = data["sub_categories"]

  tasks_html = ''
  for task in main_tasks.split("\n"):
    if len(task.strip()) == 0:
      continue       
    tasks_html = tasks_html + f'<p>{task}</p>'

  req_html = ''
  for r in req.split("\n"):
    if len(r.strip()) == 0:
      continue
    req_html = req_html + f'<p>{r}</p>'

  content_html = f'''
<div style="display: flex; margin: 10px 10px 10px 10px;">
<img style="width: 300px; height: 300px;" src="{thumb_img}"/>
<div style="margin-left: 20px;">
  <p style="text-decoration: underline; font-weight:bold;">주요업무</p>
  {tasks_html}
  <p style="text-decoration: underline; font-weight:bold;">자격요건</p>
  {req_html}
</div>
</div>
'''
  
  full_comp_html += f'''<div id="accordion">
    <div class="card">
      <div style="display:flex;" class="card-header" id="headingOne">
        <img style="width: 150px; height: 150px; align-self: center;" src="{thumb_img}"/>
        <div>
          <div style="margin: 0 0 0 20px;">
            <div style="display: flex;">
              <p style="text-decoration: underline; font-weight: bold; font-size:20px;">{name}</p> 
              <button class="btn btn-link" style="width:10px; height:10px;" data-toggle="collapse" data-target="#collapse{idx}" aria-expanded="true" aria-controls="collapse{idx}">
                자세히 보기
              </button>
            </div>
            
            <p>{",".join(sub_categories)}</p> 
            <p>{' '.join(data.get("tags", []))}</p>
          </div>
    
          
        </div>
      </div>
      <div id="collapse{idx}" class="collapse" aria-labelledby="headingOne" data-parent="#accordion">
          {content_html}
        
      </div>
    </div>
  </div>'''      
  due = data["due_time"]

components.html(full_comp_html,
  width=800,
  height=1200,
  scrolling=True
)