import streamlit as st
import pandas as pd
import base64,random
import time,datetime
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io,random
from streamlit_tags import st_tags
from PIL import Image
import pymysql
from Courses import ds_course,web_course,android_course,ios_course,uiux_course,sd_course,cs_course
import pafy
import plotly.express as px
import spacy
from itertools import chain
#import github_scrapper

spacy.load("en_core_web_sm")
def fetch_yt_video(link):
    video = pafy.new(link)
    return video.title

def get_table_download_link(df,filename,text):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    # href = f'<a href="data:file/csv;base64,{b64}">Download Report</a>'
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    return text

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def course_recommender(course_list):
    st.subheader("**Courses & Certificates🎓 Recommendations**")
    c = 0
    rec_course = []
    no_of_reco = 4
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course

def test():
    global points
    st.write("Choose the correct answer for each question:")
    start_time = time.time()


    #1
    st.write("What is the difference between 'cout' and 'printf' in C++?") 
    answer=st.selectbox("Options:",[" ",
    "'cout' is for C and 'printf' is for C++", 
    "'cout' is for C++ and 'printf' is for C", 
    "'cout' is used for formatted output and 'printf' is used for unformatted output", 
    "'cout' and 'printf' are the same"]) 
    
    if answer == "'cout' is used for formatted output and 'printf' is used for unformatted output":
        points=10
    else:
        points=0


    #2
    st.write("Write a C program to find the sum of natural numbers up to N.") 
    answer1=st.selectbox("Options:",[" ",
    "sum = (N * (N + 1)) / 2;", 
    "sum = N * (N - 1) / 2;", 
    "sum = (N * (N - 1)) / 2;", 
    "None of the above"])
    if answer1 == "sum = (N * (N + 1)) / 2;":
        points= points+10
    else:
        points=points-0
    

    #3
    st.write("What is the difference between '==' and '=' operators?")
    answer2=st.selectbox("Options:",[" ",
        "'==' is used for assignment and '=' is used for comparison", 
            "'==' and '=' are the same", 
            "'==' is used for comparison and '=' is used for assignment", 
            "'==' and '=' both are used for assignment"])
    if answer2 == "'==' is used for comparison and '=' is used for assignment":
        points= points+10
    else:
        points=points-0
        

    #4
    st.write("Which of the following Java program is to find the factorial of a number.") 
    answer3=st.selectbox("Options:",[" ",
        "int fact = 1;" 
            "for(int i = 1; i <= num; i++)" 
            "{"
                "fact *= i;"
            "}", 
        "int fact = 1;"
            "for(int i = num; i >= 1; i--)"
            "{"
                "fact *= i;" 
            "}", 
        "int fact = num * (num - 1);", 
        "None of the above"]) 
    if answer3 == "int fact = 1; for(int i = 1; i <= num; i++) {fact *= i; }":
        points= points+10
    else:
        points=points-0
    

    #5
    st.write("Write a C++ program to implement a stack using an array.")
    answer4=st.selectbox("Options:",[" ",
        "int push(int item)"
        "{"
            "if(top == MAX-1)"
                    "return -1;"
                    "else"
                        "{" 
                            "stack[++top] = item; return 0;" 
                        "}" 
        "}"
        "int pop()" 
        "{"
            "if(top == -1)" 
                "return -1;" 
                    "else"
                        "{"
                            "return stack[top--];" 
                        "}" 
        "}", 
        "Both of the above", 
        "None of the above"]) 
    if answer4 == "Both of the above":
        points= points+10
    else:
        points=points-0


    #6
    st.write("Write a C# program to check if a number is prime.")
    answer5=st.selectbox("Options:",[" ","for(int i = 2; i <= num / 2; i++) { if(num % i == 0) { isPrime = false; break; } }", 
    "for(int i = 2; i <= num / 2; i++) { if(num % i != 0) { isPrime = true; } }", 
    "Both of the above", 
    "None of the above"]) 
    if answer5 == "for(int i = 2; i <= num / 2; i++) { if(num % i == 0) { isPrime = false; break; } }":
        points= points+10
    else:
        points=points-0


    #7
    st.write("What is the importance of algorithms in problem-solving?") 
    answer6=st.selectbox("Options:",[" ", "Helps to solve problems efficiently", 
    "Not important in problem-solving", 
    "Only used in theoretical problems", 
    "None of the above"])
    if answer6 == "Helps to solve problems efficiently":
        points= points+10
    else:
        points=points-0
    

    #8
    st.write("What is a linked list?") 
    answer7=st.selectbox("Options:",[" ","A data structure with elements linked using pointers", 
    "A list of links", 
    "A list that is linked to another list", 
    "None of the above"])
    if answer7 == "A data structure with elements linked using pointers":
        points= points+10
    else:
        points=points-0


    #9
    st.write("Write the time complexity of the binary search algorithm.") 
    answer8=st.selectbox("Options:",[" ","O(1)", 
    "O(log n)", 
    "O(n)", 
    "O(n^2)"]) 
    if answer8 == "O(log n)":
        points= points+10
    else:
        points=points-0
        
    elapsed_time = time.time() - start_time
    #if elapsed_time > 60:
        #st.write("Time out!")
        #return
    st.write("Your score is", points)
    st.write("You are not qualified")
    return points
    

connection = pymysql.connect(host='localhost',user='root',password='root',db='sra')
cursor = connection.cursor()

def insert_data(name,email,res_score,timestamp,cand_level,no_of_pages,skills,recommended_skills,score,job):
    DB_table_name = 'user_data'
    insert_sql = "insert into " + DB_table_name + """
    values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    rec_values = (name, email, str(res_score), timestamp, cand_level,no_of_pages, skills,recommended_skills,score,job)
    cursor.execute(insert_sql, rec_values)
    connection.commit()

def company_signup(name,password,jobType,skills):
    DB_table='company'
    insert_sql = "insert into "+ DB_table + """ values (0,%s,%s,%s,%s)"""
    jt=name+"-"+jobType
    values=(name,password,jt,skills)
    cursor.execute(insert_sql,values)
    connection.commit()

def loginValid(username,password):
    qry="Select * from company where Name ='{}' AND Password ='{}'".format(username,password)
    cursor.execute(qry)
    data = cursor.fetchall()
    return data

def viewUsers(username):
    cursor.execute("select distinct Name,Email_ID,score from user_data where job = '{}' and score >= 60".format(username))
    data= cursor.fetchall()
    return data

def jobPostings():
    cursor.execute('select job_type from company')
    data=cursor.fetchall()
    d2=list(chain(*data))
    return d2

def fetchSkills(comp,posting):
    query="select skills_required from company where name='{}' and job_type='{}'".format(comp,posting)
    cursor.execute(query)
    data=cursor.fetchall()
    d2=list(chain(*data))
    return d2

def calculateScore(count):
    resscore=count*10
    if resscore>100:
        resscore=100
    return resscore

st.set_page_config(
   page_title="Smart Resume Analyzer",
   page_icon='./Logo/SRA_Logo.ico',
)
def run():
    st.title("Resume Analyser")
    st.sidebar.markdown("# Choose User")
    activities = ["User", "Admin","Company"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)
    # link = '[©Developed by Spidy20](http://github.com/spidy20)'
    # st.sidebar.markdown(link, unsafe_allow_html=True)
    
    # Create the DB
    db_sql = """CREATE DATABASE IF NOT EXISTS SRA;"""
    cursor.execute(db_sql)

    # Create table
    DB_table_name = 'user_data'
    table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                     Name varchar(100) NOT NULL,
                     Email_ID VARCHAR(50) NOT NULL,
                     resume_score VARCHAR(8) NOT NULL,
                     Timestamp VARCHAR(50) NOT NULL,
                     Page_no VARCHAR(5) NOT NULL,
                     Predicted_Field VARCHAR(25) NOT NULL,
                     User_level VARCHAR(30) NOT NULL,
                     Actual_skills VARCHAR(300) NOT NULL,
                     Recommended_skills VARCHAR(300) NOT NULL,
                     Recommended_courses VARCHAR(600) NOT NULL,
                     PRIMARY KEY (ID));
                    """
    cursor.execute(table_sql)
    DB_table2 ='company'
    table2_sql = "CREATE TABLE IF NOT EXISTS "+ DB_table2 + """ 
                    (ID INT NOT NULL AUTO_INCREMENT,
                    Name varchar(100) NOT NULL,
                    Password varchar(20) NOT NULL,
                    job_type varchar(100) NOT NULL,
                    skills_required varchar(100) NOT NULL,
                    PRIMARY KEY (ID));
                    """
    cursor.execute(table2_sql)

    if choice == 'User':
        # st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>* Upload your resume, and get smart recommendation based on it."</h4>''',
        #             unsafe_allow_html=True)
        
        github_url = st.text_input("Enter your github profile url").strip()

        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        if pdf_file is not None:
            # with st.spinner('Uploading your Resume....'):
            #     time.sleep(4)
            save_image_path = './Uploaded_Resumes/'+pdf_file.name
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            show_pdf(save_image_path)
            resume_data = ResumeParser(save_image_path).get_extracted_data()
            moreSkills=[]
            #if github_url !="" and len(moreSkills) == 0:
            #    skills_from_github=github_scrapper.gitHubLanguageScrapper(github_url)
            
            #    moreSkills=skills_from_github

            #full_resume_skills=resume_data['skills']+moreSkills
            if resume_data:
                ## Get the whole resume data
                resume_text = pdf_reader(save_image_path)

                st.header("**Resume Analysis**")
                st.success("Hello "+ resume_data['name'])
                st.subheader("**Your Basic info**")
                try:
                    st.text('Name: '+resume_data['name'])
                    st.text('Email: ' + resume_data['email'])
                    st.text('Contact: ' + resume_data['mobile_number'])
                    st.text('Resume pages: '+str(resume_data['no_of_pages']))
                except:
                    pass
                cand_level = ''
                if resume_data['no_of_pages'] == 1:
                    cand_level = "Fresher"
                    st.markdown( '''<h4 style='text-align: left; color: #d73b5c;'>You are looking Fresher.</h4>''',unsafe_allow_html=True)
                elif resume_data['no_of_pages'] == 2:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',unsafe_allow_html=True)
                elif resume_data['no_of_pages'] >=3:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',unsafe_allow_html=True)

                st.subheader("**Skills Recommendation💡**")
                ## Skill shows

                keywords = st_tags(label='### Skills that you have',
                text='Skills fetched from your github and resume',
                    value=resume_data['skills'],key = '1')

                ##  recommendation
                ds_keyword = ['tensorflow','keras','pytorch','machine learning','flask','streamlit','data science','data scientist','Statistics',
                                'Data Analysis','Data Visualization','Python', 'R','SQL Database',' Hadoop', 'Spark','Deep Learning','Natural Language Processing','Domain Knowledge']
                web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                               'javascript', 'angular js', 'c#', 'flask','web developer','web development','developer','java','jdbc','HTML','CSS', 'Vue.js','Git','Responsive Design',
                                'SQL', 'NoSQL']
                android_keyword = ['android','android development','flutter','kotlin','xml','kivy','android developer','android development','developer','java']
                ios_keyword = ['ios','ios development','swift','cocoa','cocoa touch','xcode','ios developer','ios development','developer']
                uiux_keyword = ['ui','prototyping','adobe photoshop','photoshop','editing','adobe illustrator','adobe indesign','indesign','uiux dveloper']
                sd_keyword=['Python', 'Java', 'C++','C','C#','problem-solving','Data Structures','Algorithms',
                                'Software Development','Git','SQL','MongoDB','APIs','Web Services','teamwork skills']
                cs_keyword=['Ethical Hacking','Network Security','Cryptography','Threat Intelligence','Incident Response','Security Assessment','Testing','Security Operations',
                            'Vulnerability Management','Security Architecture','Design','Identity','Access Management']

                test()
                if points >=45:
                    recommended_skills = []
                    reco_field = ''
                    rec_course = ''
                    ## Courses recommendation
                    activities = jobPostings()
                    activities.insert(0,'company - job profile')
                    task=st.selectbox("select company to apply for :",activities)
                    if task != 'company - job profile':
                        taskChoice=task.split("-")
                        comp=taskChoice[0]
                        jobT=taskChoice[1]
                        skillseT=fetchSkills(comp,task)
                        req_skills=skillseT[0].split(',')
                        recommended_skills = req_skills
                        recommended_keywords = st_tags(label='### Company Requirements',
                        text='Recommended skills generated from System',value=recommended_skills,key = '2')
                        for i in resume_data['skills']:
                            if jobT.lower() in ds_keyword:
                                print(i.lower())
                            #   reco_field = 'Data Science'
                                
                                st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                                rec_course = course_recommender(ds_course)
                                break

                            ## Web development recommendation
                            elif jobT.lower() in web_keyword:
                                print(i.lower())
                                reco_field = 'Web Development'
                                # recommended_skills = req_skills
                                # recommended_keywords = st_tags(label='### Company Requirements',
                                # text='Recommended skills generated from System',value=recommended_skills,key = '3')
                                st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                                rec_course = course_recommender(web_course)
                                break

                            ## Android App Development
                            elif jobT.lower() in android_keyword:
                                print(i.lower())
                                reco_field = 'Android Development'
                                # recommended_skills = req_skills
                                # recommended_keywords = st_tags(label='### Company Requirements',
                                # text='Recommended skills generated from System',value=recommended_skills,key = '4')
                                st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                                rec_course = course_recommender(android_course)
                                break

                            ## IOS App Development
                            elif jobT.lower() in ios_keyword:
                                print(i.lower())
                                reco_field = 'IOS Development'
                                # recommended_skills = req_skills
                                # recommended_keywords = st_tags(label='### Company Requirements',
                                # text='Recommended skills generated from System',value=recommended_skills,key = '5')
                                st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                                rec_course = course_recommender(ios_course)
                                break

                            # Ui-UX Recommendation
                            elif jobT.lower() in uiux_keyword:
                                print(i.lower())
                                reco_field = 'UI-UX Development'
                                # recommended_skills = req_skills
                                # recommended_keywords = st_tags(label='### Company Requirements',
                                # text='Recommended skills generated from System',value=recommended_skills,key = '6')
                                st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                                rec_course = course_recommender(uiux_course)
                                break

                            # Cybersceurity Recommendation
                            elif jobT.lower() in cs_keyword:
                                print(i.lower())
                                reco_field = 'Cybersceurity'
                                # recommended_skills = req_skills
                                # recommended_keywords = st_tags(label='### Company Requirements',
                                # text='Recommended skills generated from System',value=recommended_skills,key = '6')
                                st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                                rec_course = course_recommender(cs_course)
                                break
                        
                            # Software Developer Recommendation
                            else:
                                print(i.lower())
                                reco_field = 'Software Developer'
                                # recommended_skills = req_skills
                                # recommended_keywords = st_tags(label='### Company Requirements',
                                # text='Recommended skills generated from System',value=recommended_skills,key = '6')
                                st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                                rec_course = course_recommender(sd_course)
                                break
                        count=0
                        for i in resume_data['skills']:
                            if i.lower() in req_skills:
                                count+=1
                        score=(count/len(req_skills))*100
                        if score<50:
                            score=50
                        st.subheader("**Resume Score📝**")
                        st.markdown(
                        """
                        <style>
                            .stProgress > div > div > div > div {
                                background-color: #d73b5c;
                            }
                        </style>""",
                            unsafe_allow_html=True,
                        )
                        my_bar = st.progress(int(score))
                        st.success('** Your Resume Score: ' + str(int(score))+'**')
                            
                                #
                                ## Insert into table
                        ts = time.time()
                        cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                        cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        timestamp = str(cur_date+'_'+cur_time)

                                ### Resume writing recommendation
                                # st.subheader("**Resume Tips & Ideas💡**")
                            
                                
                                # if 'Objective' in resume_text:
                                #     resume_score = resume_score+20
                                #     st.markdown('''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Objective</h4>''',unsafe_allow_html=True)
                                # else:
                                #     st.markdown('''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add your career objective, it will give your career intension to the Recruiters.</h4>''',unsafe_allow_html=True)

                                # if 'Declaration'  in resume_text:
                                #     resume_score = resume_score + 20
                                #     st.markdown('''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Delcaration✍/h4>''',unsafe_allow_html=True)
                                # else:
                                #     st.markdown('''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Declaration✍. It will give the assurance that everything written on your resume is true and fully acknowledged by you</h4>''',unsafe_allow_html=True)

                                # if 'Hobbies' or 'Interests'in resume_text:
                                #     resume_score = resume_score + 20
                                #     st.markdown('''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies⚽</h4>''',unsafe_allow_html=True)
                                # else:
                                #     st.markdown('''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Hobbies⚽. It will show your persnality to the Recruiters and give the assurance that you are fit for this role or not.</h4>''',unsafe_allow_html=True)

                                # if 'Achievements' in resume_text:
                                #     resume_score = resume_score + 20
                                #     st.markdown('''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements🏅 </h4>''',unsafe_allow_html=True)
                                # else:
                                #     st.markdown('''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Achievements🏅. It will show that you are capable for the required position.</h4>''',unsafe_allow_html=True)

                                # if 'Projects' in resume_text:
                                #     resume_score = resume_score + 20
                                #     st.markdown('''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects👨‍💻 </h4>''',unsafe_allow_html=True)
                                # else:
                                #     st.markdown('''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Projects👨‍💻. It will show that you have done work related the required position or not.</h4>''',unsafe_allow_html=True)
                            

                        if st.button("Apply for this job"):
                            insert_data(resume_data['name'], resume_data['email'], str(0), timestamp, cand_level,resume_data['no_of_pages'], str(resume_data['skills']),
                                        str(recommended_skills),str(score),comp.strip())

                else:
                    print("You are not Qualified")
                ## Resume writing video
    #             st.header("**Bonus Video for Resume Writing Tips💡**")
    #             resume_vid = random.choice(resume_videos)
    #             res_vid_title = fetch_yt_video(resume_vid)
    #             st.subheader("✅ **"+res_vid_title+"**")
    #             st.video(resume_vid)

    #             ## Interview Preparation Video
    #             st.header("**Bonus Video for Interview👨‍💼 Tips💡**")
    #             interview_vid = random.choice(interview_videos)
    #             int_vid_title = fetch_yt_video(interview_vid)
    #             st.subheader("✅ **" + int_vid_title + "**")
    #             st.video(interview_vid)

    #             connection.commit()
    #         else:
    #             st.error('Something went wrong..')
    elif choice == "Admin":
        ## Admin Side
        st.success('Welcome to Admin side')
        # st.sidebar.subheader('**ID / Password Required!**')

        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')
        if st.button('Login'):
            if ad_user == 'JIT' and ad_password == 'jit':
                st.success("Welcome JIT")
                # Display Data
                cursor.execute('''SELECT*FROM user_data''')
                data = cursor.fetchall()
                st.header("**User's Data**")
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Resume Score', 'Timestamp',
                                                 'Cand_level','no_of_pages', 'Actual Skills', 'Recommended Skills',
                                                 'Score','job_applied_for'])
                st.dataframe(df)

                st.markdown(get_table_download_link(df,'User_Data.csv','Download Report'), unsafe_allow_html=True)

                cursor.execute('''SELECT ID, name, job_type, skills_required FROM company''')
                data2 =cursor.fetchall()
                st.header("COMPANY DETAILS")
                df2 = pd.DataFrame(data2,columns=['ID','name','job_type','skills_required'])
                st.dataframe(df2)

                ## Admin Side Data
                query = 'select * from user_data;'
                plot_data = pd.read_sql(query, connection)

                ## Pie chart for predicted field recommendations
                ##labels = plot_data.Predicted_Field.unique()
                ##print(labels)
                ##values = plot_data.Predicted_Field.value_counts()
                ##print(values)
                ##st.subheader("📈 **Pie-Chart for Predicted Field Recommendations**")
                ##fig = px.pie(df, values=values, names=labels, title='Predicted Field according to the Skills')
                ##st.plotly_chart(fig)

                ### Pie chart for User's👨‍💻 Experienced Level
                ##labels = plot_data.User_level.unique()
                ##values = plot_data.User_level.value_counts()
                ##st.subheader("📈 ** Pie-Chart for User's Experienced Level**")
                ##fig = px.pie(df, values=values, names=labels, title="Pie-Chart📈 for User's Experienced Level")
                ##st.plotly_chart(fig)

                labels = plot_data.Cand_level.unique()
                values = plot_data.Cand_level.value_counts()
                st.subheader("📈 **Pie-Chart for User's Experienced Level**")
                fig = px.pie(values=values, names=labels, title="Pie-Chart📈 for User's Experienced Level")
                st.plotly_chart(fig)



            else:
                st.error("Wrong ID & Password Provided")

    elif choice =="Company":
        st.success("Company Login/Signup")
        activities = ["Login", "Signup"]
        choice = st.sidebar.selectbox("Choose among the given options:", activities)

        if choice == "Login":
            username = st.sidebar.text_input("Company Name")
            password = st.sidebar.text_input("Password",type='password')
            if st.sidebar.checkbox("keep logged-in"):
                res= loginValid(username,password)
                if res:
                    st.success("Logged in as {}".format(username))
                    task=st.selectbox("Task",[" ","Add Job Posting","View Candidates"])
                    if task == "Add Job Posting":
                        st.subheader("Add Posting")
                        job_type = st.text_input("Job_Posting")
                        skills_required = st.text_input("skills")
                        if st.button("Add posting"):
                            company_signup(username,password,job_type,skills_required)
                            st.success("job posting added")
                    elif task=="View Candidates":
                        st.subheader("User Profiles")
                        userDetails=viewUsers(username)
                        db=pd.DataFrame(userDetails,columns=["username","Email ID","resume Score"])
                        st.dataframe(db)
                else:
                    st.warning("incorrect username/password")
        else:
            st.success("Signup")
            new_user = st.text_input("Username")
            new_password = st.text_input("Password",type='password')
            job_type = st.text_input("Job_Posting")
            skills_required = st.text_input("skills")

            if st.button("Signup"):
                company_signup(new_user,new_password,job_type,skills_required)
                st.success("Signed up successfully")
                st.info("GO to login menu")

run()