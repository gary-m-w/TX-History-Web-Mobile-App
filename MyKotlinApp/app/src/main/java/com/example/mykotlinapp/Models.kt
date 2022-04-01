package com.example.mykotlinapp

//class HomeFeed(val videos: List<MediaStore.Video>)

//class Video(val id:Int, val name:String, val link:String, val imageUrl: String, val numberOfViews: Int, val channel: Channel)
class HomeFeed(val _id:String, val address:String, val city:String, val date:String, val description:String,
               val image: String, val state: String, val tag: Array<String>,
               val theme: String, val title: String, val user: String)

//class Channel(val name:String, val profileImage: String)
//[{"_id":"6112f7056f64a74c6bede850","address":"1122 Colorado Street","city":"Austin",
//    "date":"Tue, 10 Aug 2021 22:00:37 GMT","description":"hi",
//    "image":"https://storage.cloud.google.com/texas_history_apad/6112f7056f64a74c6bede850",
//    "state":"TX","tag":["hi","hi"],"theme":"Park","title":"huihihu","user":"sophiafalco11@gmail.com"},

class ThemeFeed(val _id:String, val cover: String, val label: String)

class UserFeed(val _id:String, val email: String, val name: String, val password: String)

class checkUserFeed(val value: String)