import insta_post_extractor

# insta_man = insta_post_extractor.insta_manager("aiswarya_rajeev", 861)
# insta_man.fetch_user_info("aiswarya_rajeev")
# insta_man.fetch_profile_timeline("",0)
# anushka_bee


try:
    while(True):
        profile_name = input("Enter the insta name:")
        Post_Count = input("Enter the insta post count:")
        print("Profile Name :", profile_name)
        print("Post Count :", Post_Count)
        insta_man = insta_post_extractor.insta_manager(
            profile_name, Post_Count)
        insta_man.fetch_user_info(profile_name)
except KeyboardInterrupt:
    print("Press Ctrl-C to terminate while statement")
    pass
