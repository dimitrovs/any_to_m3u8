# any_to_m3u8
A Python script to transcode any stream to M3U8 (which can play on iOS, Android, Roku, etc.)

Note: This is very experimental. Raspberry Pi branch with transcoding enabled.

Requirements:

1) Latest Gstreamer 1.0 for Raspberry Pi with decoding licenses purchased and installed (if decoding MPEG2/VC1)

2) Python 2.7+

This script works in the following way:

1) You make a request to: http://your_any_to_m3u8_server:port/http://any_server/any_video.any_format (i.e. you just append the video stream URL after your server's URL)

2) any_to_m3u8 intercepts these URLs and starts a GStreamer process to transcode and convert your stream to M3U8

3) any_to_m3u8 redirects your player to the M3U8 file created by GStreamer

4) Your player requests the .ts chunks

5) Periodically your player requests the original URL. any_to_m3u8 detects such duplicate requests and redirects them to the M3U8 file

6) If you request a new URL, any_to_m3u8 kills GStreamer, cleans up and the process repeats from 1).

NOTE: This branch is only for the Raspberry Pi ARM-based board with dedicated hardware decoder/encoder.
