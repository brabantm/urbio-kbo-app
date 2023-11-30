# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
import streamlit as st
from streamlit.logger import get_logger
import urllib.parse

from google.oauth2 import service_account
from google.cloud import bigquery

LOGGER = get_logger(__name__)

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_companies(query):
    query_job = client.query(query)
    rows_raw = query_job.to_dataframe()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    df = rows_raw
    return df

def run():
    st.set_page_config(
        page_icon="👋",
    )
        # Get the URL query parameters
    url = st.get_option("browser.serverAddress")
    query_params = urllib.parse.urlparse(url).query
    parsed_query_params = st.experimental_get_query_params()

    # # Set the page title based on the 'title' URL parameter
    if 'buildingID' in parsed_query_params:
        
        try:
            title = str(int(float(parsed_query_params['buildingID'][0])))
            st.title("BuildingID: "+title)
        except:
            st.title("BuildingID is not a int/float")
            return
        
        rows = load_companies(f"SELECT *  FROM `elaborate-night-388209.test.urbio` WHERE `building_id` = {title} LIMIT 30")
        count = load_companies(f"SELECT COUNT(EntityNumber)  FROM `elaborate-night-388209.test.urbio` WHERE `building_id` = {title}").iloc[0,0]
        if count==0:
            st.markdown("""### Building has no company""")
            return
        else:
            st.markdown(f"""### {count} companies found""")
        maps_url = f"https://www.google.com/maps/embed/v1/place?zoom=18&q={rows.loc[0,'lat_urbio']},{rows.loc[0,'lon_urbio']}&key=AIzaSyAqriQ2C8n_ql4HrJFB5tyEdY_36tYT77k"
        st.components.v1.iframe(maps_url, width=None, height=300, scrolling=False)

        rows["OTB"] = "<a href='https://openthebox.be/company/BE" + rows["EntityNumber"].str.replace(".", "")+"'>OTB</a>"
        rows["Bizzy"] = "<a href='https://bizzy.org/en/be/" + rows["EntityNumber"].str.replace(".", "")+"'>Bizzy</a>"

        # st.dataframe(rows[["EntityNumber", "Denomination", "OTB"]])
        st.markdown(rows[["EntityNumber", "Denomination", "OTB", "Bizzy"]].to_html(render_links=True, escape=False),unsafe_allow_html=True)

        
      
    else:
        
        st.title("hello")
        
        
    # st.sidebar.success("Select a demo above.")

    # st.markdown(
    #     """
    #     Streamlit is an open-source app framework built specifically for
    #     Machine Learning and Data Science projects.
    #     **👈 Select a demo from the sidebar** to see some examples
    #     of what Streamlit can do!
    #     ### Want to learn more?
    #     - Check out [streamlit.io](https://streamlit.io)
    #     - Jump into our [documentation](https://docs.streamlit.io)
    #     - Ask a question in our [community
    #       forums](https://discuss.streamlit.io)
    #     ### See more complex demos
    #     - Use a neural net to [analyze the Udacity Self-driving Car Image
    #       Dataset](https://github.com/streamlit/demo-self-driving)
    #     - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    # """
    # )


if __name__ == "__main__":
    run()
