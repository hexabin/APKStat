# APKStat
Save time during your initial analysis of an Android APK file. APK Stat will grab most of the information you need in your initial assessment right away and output the information in an easy to read set of text files.

<strong>USAGE</strong>: python apkstat.py yourapkfile.apk


<strong><i>Dependancy:</i></strong> APKTool - <a href="https://ibotpeaches.github.io/Apktool">https://ibotpeaches.github.io/Apktool/</a>


<h2><strong>APK Stat - Basic APK Information Grabber for Android Malware Analysis</strong></h2>

APK Stat will use APK Tool to decompress and decode your APK file. APK Stat Will:
<ul>
<li> Breaks Permissions, Activities, Activity Aliases, Services, Providers and Receivers Into Easily Readable Groups</li>
<li> Scours All Files After Decoding For Hardcoded IP Addresses and Domain Names</li>
<li> Single Out The Launcher Activity </li>
<li> Automatically Creates a Strings.txt file</li>
</ul>
