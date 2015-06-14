# any_to_m3u8
A Python script to transcode any stream to M3U8 (which can play on iOS, Android, Roku, etc.)

Note: This is very experimental.

Requirements:

1) Latest FFMPEG (I suggest you download the Static build from here: http://johnvansickle.com/ffmpeg/)

2) Python 2.7+

This script works in the following way:

1) You make a request to: http://your_any_to_m3u8_server:port/http://any_server/any_video.any_format (i.e. you just append the video stream URL after your server's URL)

2) any_to_m3u8 intercepts these URLs and starts an FFMPEG process to convert your stream to M3U8

3) any_to_m3u8 redirects your player to the M3U8 file created by FFMPEG

4) Your player requests the .ts chunks

5) Periodically your player requests the original URL. any_to_m3u8 detects such duplicate requests and redirects them to the M3U8 file

6) If you request a new URL, any_to_m3u8 kills FFMPEG, cleans up and the process repeats from 1).

NOTE: This experimental version has TRANSCODING (eg. MPEG2 to H264 for example) DISABLED. However, it is trivial to enable (if you have the necessary CPU resources). Message me for instructions.
