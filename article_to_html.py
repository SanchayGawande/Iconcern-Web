import random
import string
from jinja2 import Template,Environment, FileSystemLoader


def create_div_ids(data):
     letters = string.ascii_uppercase
     for i in range(1,8):
        div_id=''.join(random.choice(letters) for _ in range(3))
        data['sub_heading_tag_'+'{}'.format(i)]=div_id
     return data

def json_to_html(data):
    print(data,type(data))
    # Load JSON data
    # data = json.loads(json_data)
    data=create_div_ids(data)
    # print(data)
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ title }}</title>
        {% include 'header.html' %}
     
    </head>
    <body>

    <div class="row ">
 		<div class="col-md-12 fadeIn animate-onscroll">
            <h2 class="title-style-2"> Tabs <span class="title-under"></span></h2>
                <div role="tabpanel">
                    <ul class="nav nav-tabs" role="tablist">
    					<li role="presentation" class="active"><a href="#{{ sub_heading_tag_1 }}" aria-controls="home" role="tab" data-toggle="tab">{{sub_heading_1}}</a></li>
    					<li role="presentation"><a href="#{{ sub_heading_tag_2 }}" aria-controls="profile" role="tab" data-toggle="tab">#{{ sub_heading_tag_2 }}</a></li>
    					<li role="presentation"><a href="#{{ sub_heading_tag_3 }}" aria-controls="messages" role="tab" data-toggle="tab">{{ sub_heading_tag_3 }}</a></li>
    					<li role="presentation"><a href="#{{ sub_heading_tag_4 }}" aria-controls="settings" role="tab" data-toggle="tab">{{ sub_heading_tag_4 }}</a></li>
                        <li role="presentation"><a href="#{{ sub_heading_tag_5 }}" aria-controls="settings" role="tab" data-toggle="tab">{{ sub_heading_tag_5 }}</a></li>
                        <li role="presentation"><a href="#{{ sub_heading_tag_6 }}" aria-controls="settings" role="tab" data-toggle="tab">{{ sub_heading_tag_6 }}</a></li>
                        <li role="presentation"><a href="#{{ sub_heading_tag_7 }}" aria-controls="settings" role="tab" data-toggle="tab">{{ sub_heading_tag_7 }}</a></li>
    				</ul>
                </div>
        </div>
    </div>

    <main>
            <h2>{{ sub_topic_1 }}</h2>
            <p><em>Author: {{author}}</em></p>
            <p>{{ sub_topic_1_description }}</p>

"""
    for key, val in data.items():
            if val is None:
                #  print(key)
                 continue
            if key=='sub_topic_2_description' and val is not None:
                 html_template +='''
            <h2>{{ sub_topic_2 }}</h2>
            <p>{{ sub_topic_2_description | safe }}</p> '''
                 
            elif key=='sub_topic_3_description' and val is not None:
                 html_template +='''
            <h2>{{ sub_topic_3 }}</h2>
            <p>{{ sub_topic_3_description | safe }}</p> ''' 
                 
            elif key=='sub_heading_1_description' and val is not None:
                 html_template +='''
            <div id={{sub_heading_tag_1}}>     
            <h2>{{ sub_heading_1 }}</h2>
            <p>{{ sub_heading_1_description | safe }}</p> 
            </div>''' 

            elif key=='sub_heading_2_description' and val is not None:
                 html_template +='''
            <div id={{sub_heading_tag_2}}>     
            <h3>{{ sub_heading_2 }}</h3>
            <p>{{ sub_heading_2_description | safe }}</p> 
            </div>''' 
                 
            elif key=='sub_heading_3_description' and val is not None:
                 html_template +='''
            <div id={{sub_heading_tag_3}}>    
            <h3>{{ sub_heading_3 }}</h3>
            <p>{{ sub_heading_3_description | safe }}</p>  
            </div>''' 

            elif key=='sub_heading_4_description' and val is not None:
                 html_template +='''
            <div id={{sub_heading_tag_4}}> 
            <h3>{{ sub_heading_4 }}</h3>
            <p>{{ sub_topic_4_description | safe }}</p> 
            </div>''' 

            elif key=='sub_heading_5_description' and val is not None:
                 html_template +='''
            <div id={{sub_heading_tag_5}}>    
            <h3>{{ sub_heading_5 }}</h3>
            <p>{{ sub_heading_5_description | safe }}</p> 
            </div>''' 
                 
            elif key=='sub_heading_6_description' and val is not None:
                 html_template +='''
            <div id={{sub_heading_tag_6}}>    
            <h3>{{ sub_heading_6 }}</h3>
            <p>{{ sub_heading_6_description | safe }}</p>  
            </div>''' 
                 
            elif key=='sub_heading_7_description' and val is not None:
                 html_template +='''
            <div id={{sub_heading_tag_7}}>    
            <h3>{{ sub_heading_7 }}</h3>
            <p>{{ sub_heading_7_description | safe }}</p>  
            </div>
            </main>
            </body>
            </html>
            '''

    # Create a Jinja2 template object
    template = Template(html_template)
    print(template)

    # Render HTML with JSON data
    html_output = template.render(title=data["sub_topic_1"],
                                  author=data["author"],
                                  sub_topic_1=data["sub_topic_1"],
                                  sub_topic_1_description=data["sub_topic_1_description"],
                                  sub_topic_2=data["sub_topic_2"],
                                  sub_topic_2_description=data["sub_topic_2_description"],
                                  sub_topic_3=data["sub_topic_3"],
                                  sub_topic_3_description=data["sub_topic_3_description"],
                                  sub_heading_1=data["sub_heading_1"],
                                  sub_heading_1_description=data["sub_heading_1_description"],
                                  sub_heading_2=data["sub_heading_2"],
                                  sub_heading_2_description=data["sub_heading_2_description"],
                                  sub_heading_3=data["sub_heading_3"],
                                  sub_heading_3_description=data["sub_heading_3_description"],
                                  sub_heading_4=data["sub_heading_4"],
                                  sub_heading_4_description=data["sub_heading_4_description"],
                                  sub_topic_4=data["sub_topic_4"],
                                  sub_topic_4_description=data["sub_topic_4_description"],
                                  sub_heading_5=data["sub_heading_5"],
                                  sub_heading_5_description=data["sub_heading_5_description"],
                                  sub_heading_6=data["sub_heading_6"],
                                  sub_heading_6_description=data["sub_heading_6_description"],
                                  sub_heading_7=data["sub_heading_7"],
                                  sub_heading_7_description=data["sub_heading_7_description"],
                                  sub_heading_tag_7=data["sub_heading_tag_7"],
                                  sub_heading_tag_6=data["sub_heading_tag_6"],
                                  sub_heading_tag_5=data["sub_heading_tag_5"],
                                  sub_heading_tag_4=data["sub_heading_tag_4"],
                                  sub_heading_tag_3=data["sub_heading_tag_3"],
                                  sub_heading_tag_2=data["sub_heading_tag_2"],
                                  sub_heading_tag_1=data["sub_heading_tag_1"])
    # print(html_output)
    return html_output







# <div class="row ">

# 				<div class="col-md-12 fadeIn animate-onscroll">

# 					<h2 class="title-style-2"> Tabs <span class="title-under"></span></h2>

					
# 						<div role="tabpanel">

# 							  <!-- Nav tabs -->
# 							  <ul class="nav nav-tabs" role="tablist">
# 							    <li role="presentation" class="active"><a href="#home" aria-controls="home" role="tab" data-toggle="tab">Home</a></li>
# 							    <li role="presentation"><a href="#profile" aria-controls="profile" role="tab" data-toggle="tab">Profile</a></li>
# 							    <li role="presentation"><a href="#messages" aria-controls="messages" role="tab" data-toggle="tab">Messages</a></li>
# 							    <li role="presentation"><a href="#settings" aria-controls="settings" role="tab" data-toggle="tab">Settings</a></li>
# 							  </ul>

# 							  <!-- Tab panes -->
# 							  <div class="tab-content">
# 							    <div role="tabpanel" class="tab-pane active" id="home">
# 							    	Lorem ipsum dolor sit amet, consectetur adipisicing elit. In consequatur mollitia, libero quisquam impedit obcaecati, dignissimos, eum similique minima ab amet eos sequi distinctio qui modi? Possimus quos, fugit quia.</div>
# 							    <div role="tabpanel" class="tab-pane" id="profile">
# 							    	Lorem ipsum dolor sit amet, consectetur adipisicing elit. Molestiae aut culpa a commodi. Quidem asperiores aliquid sequi incidunt quas soluta eum ab fugiat deleniti in at iste, illum ipsam nisi.</div>
# 							    <div role="tabpanel" class="tab-pane" id="messages">
# 							    	Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ex aliquam corrupti quibusdam nostrum, aspernatur iure illo, alias vitae, reiciendis culpa explicabo minus iusto ipsum cum tempore incidunt iste praesentium nihil.</div>
# 							    <div role="tabpanel" class="tab-pane" id="settings">
# 							    	Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ea ducimus ullam distinctio fugiat voluptates! Vero quis adipisci asperiores aliquam ullam doloremque dolor, reprehenderit, accusamus nisi ut eveniet quas reiciendis dolore.</div>
# 							  </div>

# 						</div>

# 						<p></p>
					

# 				</div>

# Example JSON data
# json_data_example ={
#     "_id": {"$oid": "655e8820e63d2a14f5b8ceb0"},
#     "id": {"$numberInt": "1"},
#     "link": "https://www.heart.org/en/health-topics/diabetes",
#     "author": "American Heart Association",
#     "topic": "Diabetes",
#     "description": None,
#     "sub_topic_1": "What is Diabetes?",
#     "sub_topic_1_description": "Diabetes, also called diabetes mellitus, is a condition that causes blood sugar to rise. Diabetes is diagnosed based on a fasting blood glucose (sugar) level of 126 milligrams per deciliter (mg/dL) or higher.",
#     "sub_topic_2": "How diabetes develops",
#     "sub_topic_2_description": "When your digestive system breaks down food, your blood sugar level rises. The body’s cells absorb the sugar (glucose) in the bloodstream and use it for energy. The cells do this using a hormone called insulin, which is produced by the pancreas, an organ near the stomach.<br><br>When your body doesn’t produce enough insulin and/or doesn’t efficiently use the insulin it produces, sugar levels rise in the bloodstream. As a result:<br><br>Right away, the body’s cells may be starved for energy.<br>Over time, high blood glucose levels may damage the eyes, kidneys, nerves or heart.",
#     "sub_topic_3": "Types of diabetes",
#     "sub_topic_3_description": None,
#     "sub_heading_1": "Type 1 diabetes",
#     "sub_heading_1_description": "This type of diabetes is also referred to as insulin-dependent diabetes. People with Type 1 diabetes must take insulin or other medications daily. This makes up for the insulin not being produced by the body.<br><br>Type 1 diabetes was previously known as juvenile diabetes because it’s usually diagnosed in children and young adults. However, this chronic, lifelong condition can strike at any age. People with a family history of Type 1 diabetes have a greater risk of developing it.",
#     "sub_heading_2": "Health risks for Type 1 diabetes",
#     "sub_heading_2_description": "Type 1 diabetes develops when the body’s immune system attacks and destroys cells in the pancreas that make insulin.<br><br>Once these cells are destroyed, the pancreas produces little or no insulin, so glucose stays in the blood. When there’s too much glucose in the blood, especially for prolonged periods, the organ systems in the body suffer long-term damage.",
#     "sub_heading_3": "Type 2 diabetes",
#     "sub_heading_3_description": "Type 2 diabetes is the most common form of diabetes. Type 2 diabetes has historically been diagnosed primarily in adults. But adolescents and young adults are developing Type 2 diabetes at an alarming rate because of family history and higher rates of obesity and physical inactivity — risk factors for Type 2 diabetes.<br><br>This type of diabetes can occur when:<br><br>The body develops “insulin resistance” and can’t efficiently use the insulin it makes.<br>The pancreas gradually loses its capacity to produce insulin.<br><br>In a mild form, this type of diabetes can go undiagnosed for many years. That’s cause for concern since untreated diabetes can lead to many serious medical problems including cardiovascular disease.<br>Type 2 diabetes may be delayed or controlled with diet and exercise.<br>With the exception of gestational diabetes, diabetes that happens for the first time during pregnancy, once a body becomes diabetic, diet and health management will be a life-long process.<br>If you’ve been diagnosed with diabetes, it’s important to follow your health care professional’s recommendations and take all medications as directed. It’s also important to commit to making healthy diet and lifestyle changes that can help manage your condition and slow its progression.",
#     "sub_heading_4": None,
#     "sub_heading_4_description": None,
#     "sub_topic_4": "Precursors to diabetes",
#     "sub_topic_4_description": None,
#     "sub_heading_5": "Insulin resistance",
#     "sub_heading_5_description": "Insulin resistance occurs when the body makes insulin but can’t use it efficiently. This means that glucose builds up in the bloodstream instead of being used by cells.<br><br>To reduce the high blood sugar levels, the insulin-producing cells in the pancreas release more and more insulin to try to keep blood sugar levels normal. Gradually, these cells fail to keep up with the body’s need for insulin. As a result, blood sugar levels begin to rise.<br><br>When a fasting person has too much glucose in the blood (hyperglycemia) or too much insulin in the blood (hyperinsulinemia), they may have insulin resistance.",
#     "sub_heading_6": "Health risks of insulin resistance",
#     "sub_heading_6_description": "People with insulin resistance are at greater risk of developing prediabetes, Type 2 diabetes and cardiovascular disease.<br><br>People with insulin resistance are more likely to have a history of being obese and physically inactive. They are also likely to have other cardiovascular risk factors such as too much LDL (bad) cholesterol, not enough HDL (good) cholesterol, high triglycerides and high blood pressure.<br><br>That’s why it’s important to be aware of diabetes risk factors and take steps to prevent diabetes.",
#     "sub_heading_7": "Prediabetes",
#     "sub_heading_7_description": "Prediabetes means the body is having trouble getting your blood sugar down to a healthy range, but it hasn’t yet reached the level of Type 2 diabetes.<br><br>If you’ve been told by your doctor that you have prediabetes, you can reduce your risk of developing Type 2 diabetes by improving your diet, increasing your physical activity and losing weight if you are overweight."
# }

# html_output = json_to_html(json_data_example)

# # Save HTML to a file or print it
# with open('output.html', 'w') as html_file:
#     html_file.write(html_output)