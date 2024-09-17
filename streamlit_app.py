import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter, SRTFormatter

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("💬 Youtube Curator Chatbot")
st.write("Please insert youtube URL or video_id you want to analyze and talk in the textbox (as shown in the example):")

raw_video_str = st.text_input("List of youtube video id or URL, separated by comma", 
                           "f2IvZ7EJgts, _cqwni4eUGU, 4YhP4QZhAJc, https://www.youtube.com/watch?v=0_lDtF8X-C0")

language_flag = st.checkbox("Specify language of each clip (if not English)", value=True)
if language_flag:
    st.write("Please specify the language of each clip if not English (default: English):")
    language_str = st.text_input("Support only acronym like 'en', 'th', 'jp', ...", 
                           "th, th, th, th")
    # st.write(language_str)
    lang_list = language_str.split(',')
    lang_list = [lang.strip() for lang in lang_list]
else:
    lang_list = []

raw_video_list = raw_video_str.split(',')
raw_video_list = [v.strip() for v in raw_video_list]
video_id_list = []
for r in raw_video_list:
    if "http" in r:
        youtube_id = r.split('v=')[-1]
        video_id_list.append(youtube_id)
    else:
        video_id_list.append(r)

ready_flag = st.checkbox("Check if all information is ready", value=False)

if ready_flag:
    # Get youtube transcript
    transcript_raw_list = []
    for i, id in enumerate(video_id_list):
        try:
            lang = lang_list[i]
        except:
            lang = 'en'
            
        try:
            ret = YouTubeTranscriptApi.get_transcript(id, languages=[lang])
            transcript_raw_list.append(ret)
        except Exception as e:
            st.write(f"Could not get the transcript for video ID: {id} - please verify the ID or specified language or URL")
            st.write(e)

    st.write(f'** Total {len(transcript_raw_list)} valid clips where transcripts were successfully extracted**')
    if len(transcript_raw_list) > 0:
        with st.chat_message("assistant"):
            for i, script in enumerate(transcript_raw_list):
                st.write(f"### source {i}")
                st.write(script)
    
# if not openai_api_key:
#     st.info("Please add your OpenAI API key to continue.", icon="🗝️")
# else:

#     # Create an OpenAI client.
#     client = OpenAI(api_key=openai_api_key)

#     # Create a session state variable to store the chat messages. This ensures that the
#     # messages persist across reruns.
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Display the existing chat messages via `st.chat_message`.
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     # Create a chat input field to allow the user to enter a message. This will display
#     # automatically at the bottom of the page.
#     if prompt := st.chat_input("What is up?"):

#         # Store and display the current prompt.
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         # Generate a response using the OpenAI API.
#         stream = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": m["role"], "content": m["content"]}
#                 for m in st.session_state.messages
#             ],
#             stream=True,
#         )

#         # Stream the response to the chat using `st.write_stream`, then store it in 
#         # session state.
#         with st.chat_message("assistant"):
#             response = st.write_stream(stream)
#         st.session_state.messages.append({"role": "assistant", "content": response})
