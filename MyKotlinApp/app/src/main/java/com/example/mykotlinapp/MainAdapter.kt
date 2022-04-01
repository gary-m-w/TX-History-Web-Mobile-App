package com.example.mykotlinapp

import android.content.Intent
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.squareup.picasso.Picasso
import kotlinx.android.synthetic.main.video_row.view.*


class MainAdapter(val homeFeed: Array<HomeFeed>): RecyclerView.Adapter<MainAdapter.CustomViewHolder>() {

    //val videoTitles = listOf("First","Second","Third","Fourth")
    override fun getItemCount(): Int {
        return homeFeed.count()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CustomViewHolder {
        val layoutInflater = LayoutInflater.from(parent?.context)
        val cellForRow = layoutInflater.inflate(R.layout.video_row, parent, false)
        return CustomViewHolder(cellForRow)
    }

    override fun onBindViewHolder(holder: CustomViewHolder, position: Int) {
        // val videotitles = videoTitles.get(position)
        val video = homeFeed.get(position)
        holder?.view?.textView_video_title?.text = video.description.toString()

        holder?.view?.textView_channel_name?.text = "Address: " + video.address.toString()

        holder?.view?.textView4?.text =
            "                   " + video.city.toString() + video.state.toString()

        holder?.view?.textView6?.text = "Theme: " + video.theme.toString()

        holder?.view?.textView7?.text = video.title.toString()

        val sb = StringBuilder()
        for (element in video.tag) {
            sb.append("#").append(element).append(", ")
        }
        val final_tag = sb.toString().substring(0, sb.length-2)
        holder?.view?.textView8?.text = "Tags: "+final_tag

        val thumbnailImageView = holder?.view?.imageView_video_thumbnail
        Picasso.get().load(video.image).into(thumbnailImageView)


    }



    class CustomViewHolder(val view: View): RecyclerView.ViewHolder(view) {
        init {
            view.setOnClickListener{


                val intent = Intent(view.context,ThemeActivity::class.java)

                view.context.startActivity(intent)
            }
        }
    }
}