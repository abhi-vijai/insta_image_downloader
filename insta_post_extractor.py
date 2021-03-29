import requests
import json
import urllib.request
import os
import save_image
import time


class insta_manager:
    def __init__(self, user_name, count):
        self.user_name = user_name
        self.user_id = ""
        self.count = int(count)

    def fetch_user_info(self, profile_name):
        url = "https://www.instagram.com/"+profile_name+"/?__a=1"
        response = requests.request("GET", url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)\
AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}, data={})
        #print("response::::", response.text)
        response_json = json.loads(response.text)
        user_data = response_json.get("graphql").get("user")

        self.user_id = user_data.get("id")
        begin = time.time()

        self.fetch_profile_timeline("", 0)
        end = time.time()
        final_time = end - begin
        print(final_time)

    def fetch_profile_timeline(self, after, postion):
        print("fetch_profile_timeline")
        if postion < self.count:
            if after != "":
                after = ",\"after\":\""+after+"\""
            print("postion:::", postion)
            url = "https://www.instagram.com/graphql/query/?query_hash=56a7068fea504063273cc2120ffd54f3&variables={\"id\":\"" + \
                self.user_id+"\",\"first\":40"+after+"}"
            time.sleep(postion/10)
            response = requests.request("GET", url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)\
AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}, data={})
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36
            print(response)
            timeline_json = json.loads(response.text)

            self.fetch_post(((timeline_json.get("data")).get("user")).get(
                "edge_owner_to_timeline_media"), postion)

    def fetch_post(self, timeline_data, current_position):
        print("fetch_post")
        timeline_post_count = timeline_data.get("count")
        next_page_info = timeline_data.get("page_info")
        edges = timeline_data.get("edges")
        for position in range(len(edges)):
            post_data = edges[position].get("node")

            if "edge_sidecar_to_children" in post_data:
                print("Multiple Card Present")
                edge_sidecar_to_children = post_data.get(
                    "edge_sidecar_to_children").get("edges")
                for child_key in range(len(edge_sidecar_to_children)):
                    child_card = (
                        edge_sidecar_to_children[child_key]).get("node")
                    save_image.save_the_images_in_local(post_data.get(
                        "id"), child_card.get("display_url"), self.user_name)
            else:
                save_image.save_the_images_in_local(post_data.get(
                    "id"), post_data.get("display_url"), self.user_name)

        if timeline_post_count > current_position:
            final_postion = current_position+len(edges)
            print("final_postion:::::", final_postion)
            if(next_page_info.get("has_next_page")):
                self.fetch_profile_timeline(
                    next_page_info.get("end_cursor"), final_postion)
