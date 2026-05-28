SO yeah i was making face_to_anime but gotb overwhelmed by how much things i need to learn b4 making that hence wanted to work on something light and cool: `virtual joystick!`
So at first i wrote the basic code to track hand using mediapipe and wasn't sure how I can i do it excatly but we'll se later aayugewvfduy4ebfh

------------

The very first task I have to do now is to decide the controls. I have to make it confortable for player hence thinking to make it one hand only(left or right: what user is confortable in)

I think controls should be customizeable 
but for now I am making for **Minecraft**:
- WSAD - Hand forward, backward, left, right
- Jump - Hand up
- Shift - Hand down
- Left Click - Pinch thumb and index finger
- Rigt Click - Pinch thumb and middle finger
- Sprint - Hand Forward then rest then farward (under 1 sec)

There will also be a rest pose that keeps player in rest..
We might use other hand for config like for pause, for camera move change and other configs

------------

So after deciding controls, its time to implement! First task is to assign a rest pose of hand.
For this I used off hand: if it shows thumb up, the program will check, if main hand is present, if no so rest pose is blank or else it will check if all 21 landmarks of main hand is present, if yes, it will set the landmark of main hand as rest pose and will show in red.
I chose red color to differentiate from my live hands.

------------

It would be interesting - So my target was to measure the diff b/w rest_pose_hand ldms and current hand ldms so as to i can track the movement and do WASD, for this i had to firstly find out, what ldms we will use to find the diff first. At first i thought i should do of all ldms but that would be too much so i thought to use the center of hand.

For this i thought to find center of 0 - 12 and 4 - 20 then find the center of those both. I spent so much time to find the center and even did but didn't have idea on how to find center of those center point.. But soon i realized if we draw an imaginery line from 0-12 and 4-20, the intersection point will be center and when i did, it worked! but after spending hours, i realized 9 was close to the center, and my solution might be bad suppose if hand if lil bend but 9 will alays be near center and will stay at same place, hence i wasted my day

I also learned that sometime perfect is not what we need rather we need something that can work fast and reliably

------------

It was pretty ez, i just had to find the diff between rest pose and current hand ldm's. Though for threshold i was running my mind too much but it was simple

------------

python-uinput was already downloaded, just had to implement as shown in docs. Ran into some permission and module err but was working good at last. RIght now on every frame, it is pressing and releasing the key but eaglercraft(minecraft clone on browser) is not accepting it, afaik it might be either due to it is too fast that eaglercraft can't handle or eaglercraft is blocking it. 

So next time i may wanna try another module or trynna read more docs in it and see how i can keep it press until another key is not popped..

------------

So as i thought, eaglercraft was looking for press and release key instead of just click. At first i tried looking for something like that in python-uinput but there wasn't ig, so i moved to pynput which was surprisingly easier to work with as i didn't have to load uinput as well as it does the same thing press and release.

Then soon i implemented it and i was successfully able to do left, right, jump and sneak.

But there are some known issues and tasks:
 - The keys and mouse(input devices) doesn't work properly after i run pynput idk why, need to restart computer everytime i run it..
 - Rn it supports one key at a time only but we need combinations as well..
 - When i do right, it happens left and vice versa, i think i should flip the image 180 deg vertically to make it right, we'll see it later..

But b4 solving problems blindly, i should update readme with plans and everything and focus on what will make it work.

------------

So now we can do combinations as well! Just had to convert key from string to list and change some relevent code.

I think now i should focus on these issues: the input devices work weird after running the program and mirror

------------

So for quiting i saw it was occuring most of the time when i was switching window to shut it down and i guessed break was just breaking the loop not completely stopping it hence i added a gesture(thumb down in right hand) by which it will quit the program(most of the time it works but still buggy)

Mirroring was also ez, i just had to flip the img horizontally using cv2.flip

So now lets focus on depth! for forward and backward

------------

This was very interesting! So since i had to know the depth diff between rest pose hand and current hand, i had many ways to find it, i might have also utilized the z axis in landmark we get but i found it not that accurate then i thought i can measure the diameter(i donno if it is right word for polygonal) horizontally or vertically and then find the difference!
AT first i thought to use horizontal but soon realized it wouldn't be accurate as it changed dramatically if user stretches hand lil bit so decided to do vetically(0 and 12) which is much more stable.
Then after doing the same thing as i did with A and S, i was able to to W and S!

But till this point, just guessing the hand position and trynna move and see was so annoying, i wanted the cv screen on my screen while playing.
And most of the time, the input devices are no working when i try to shut down the program without keeping it in the rest pose..

-----------

After doing 5 min of research i found a very imple way to pin the window, actually it is built in, in most of te linux just right click on title and click "Always on top". 
But my image was too big, at first had to make it smaller.

After scaling the image, i found there is a toolbar which is acquiring too much space ut completely useless but after asking at stackoverflow, one man answered and used namedWindow: autoresize | gui_normal

But even now having to pin it manually and send it to correct desktop..
I also tried to play game: not that correct ngl, i tried playing bedwar(just wasd and jump/sneak) even though whie waking on bridge, just fell of lol. 
Lets firstly implment rest of the controls then make it accurate and better

-----------

So now during making click gesture, i realized, how much ambiguous it will be with W and S, bcz when i try to connect thumb and index finger or middle finger, the landmark that triggers w and s also moves.. Which is why we needed to move to a more stable way. i found we shouldn't use fingers' landmark at all, we should use palm's.
So at first i tried to do the bottom of middle finger(9) and wrist(0) for w and s. but when i was trynna do right click gesture(not yet implmented), it was affecting even 9.. then i moved to wrist and pinky finger as they were most unaffected(we can always change it later when needed)

Also i am now releasing current keys before quitting so as to i will not need to get it to be in rest pose before making it stop working. AM using thumb down from off hand as gesture to quit..

-----------

So for left clicking i need to measure whether user is pinching or not using index or middle finger, for i made a new file samples/finger_join.py that finds the hlm of both tip(index finger and thumb) then multiply with the width and hight of the image to get pixel value from 0-1 as we need this. Then i got to know we can use norm function to find the distance between 2 points, simply did that and got! When i was pinching, the value was going below 20. `Then during that i realized i was finding the distance for w and s as well, i think later we can implement norm there too..`

For left clicking i realized we do both high cps click and one time click without realising(like during mining), so it means we need 2 different gestures for left click:
- High CPS: Pinch thumb + index finger(it will autoclick until u hold it)
- Hold Click: Pinch thum + middle finger

Yeah we are using both for left click, we'll see for right click later..

-----------

So after getting idea of what i wanna do, i wrote the logic for mouse that detects if its an index pinch or middle pinch. AT first i implemented clicking logic for just middle pinch as it was hold mouse click which was easier: just press and release

Now it was time for high cps and tbh till this point i realized i was making something similar to cheat client as i was supporting autoclicking on right click lol, but what else can i do? i can't just ask my user to move his fingers to fast to gain 6cps, neither it will track so fast. But to avoid being marked as cheat, i kept the cps lil randomized like first click was 100ms so next might be like 85 and next would be 147 etc.(with a max fector like sum or do difference by a factor(0.2 rn))

After that i got a problem, i want it to run it as independant while loop that triggers a start and an end

After asking it in discord, i got to know that i should use threading and after learning abt it a bit, i implemented it as well though it was lil tough but i did that: There was a global variable that tracks whether the cps is started or not and based on that it starts or end. I create thread everytime i end then start as we cannot reuse the same thread unfort.

-----------

Right click also had 2 mode: press and release(like during eating) and click(like placing blocks, trade with villager etc etc).

Instead of making it a complete different gesture, i made it same to left click gesture, but also a off hand gesture that tells its for right click:

- Hold Right Click = (Pinch thumb + middle finger) + Off hand gesture
- Right Click CPS = (Pinch thumb + index finger) + Off hand gesture

For now i kept open palm as Off hand gesture but we may chane later.

It was simple to implement as most of the logic were written i jst had to make a global variable that checks if off hand palm is opened or close, then during event triggers lie press release, pass a btn variable as arg that is Button.left if off palm is close or else Button.right.,

So till now we have made a basic version of what we want, but the code looks really messy and unorganized, hence my next aim would be to structuralize code and lil optimize ig

-----------

Srry for late commits and logs.
So i have modularized and made code much better and solved some bug.
At first commit, I created files for major components like camera, constants etc. and seperated them in diff folders.
In second commit(writte fix:), i made the most part modular, solved issues.
In third commit i solved quit and release function as it was lil wrong.
And at last commit(this), i wrote the logs, made the main.py better and structured!

Later we may also make tests file to check...
So now we can do right/left click and WASD and jump/sneak.

Now we have to work on rest of the things like sprint, rotation and switching inventory.

-----------

So for sprint i chose W then rest pose then W under 1 sec as it is familiar to sprint mode.
i had to write some seperate logic as unlike rest of the keys(WASD/space/shift), it doesn't show the gesture every frame rather it shows first time only when we do W then rest then W and remove when we do back or w is cancelled.
At first i wrote logic of timestamps to see last forward(w) time, last rest pose time and current time(when w is pressed), then i calculate if time between last forward time and current time is less than 1 second and we did rest pose in between, then do sprint. I used a global variable(`self.sprint`) to store current state then every frame i check if `self.sprint` is true and W is in current keys, then do `self.current_keys.append("R")`(r is sprint key) or else if w not in current keys but `self.sprint` is True, then `self.sprint = False`

And it worked! now lets do the harder part: switching inventory

-----------

So now we had to choose the gesture for switching inventory, i wanted it to feel natural hence i chose to do little right/left move then back to center under 1 sec. But it might conflict with A and D key, hence i chose to set a distance like: if hand is moved to right or left under 10%, it is for inventory or else it if for A and D.

I hadn;t written the logic yet, but for switching inventory, i would be using mouse.scroll, but my code was hardcoded for right and left click only, hence i had to rewrite the code to store key types in array instead of individual only. will write the inventory logic next

-----------

This took 2 attempts to be done, this log is for successful attempt.. So at first i worked on gesture_mapper.py where i wrote the logics to do these: First made a new global state as last_horizontal_move_for_inventory that stores the side and time of last time we moved to left or right and their i added a dummy keyboard.append as I wanted this move to count as busy not rest post. Then in b4 setting last_rest_pose_time, i check if current rest pose time and last rest pose time if under 1 second and between them, there is time of last horizontal move, it means user is trying to switch inventory then check the side and append in current_mouse_btn_types. In actions_taker.py, i check if prev_inventory or next_inventory is in the arr, if yes do mouse.scroll (1 or -1 based on side). thats it!

Now we have to do a much harder one: Rotation, as we have to rotate in all side.. And recently i got to know, for this we will be moving cursor and we also need to move cursor for like trading with villager or managing inventory(need to hold the items as well), but lets firstly focus on simpler rotation..

-----------

So now rotation hehe, must be hard but lets decide the gesture or trigger for it first. So ig the rotating the hand would convinient, but sometimes i dont want it to be so slow neither so fast, wt abt setting the speed of rotation manually? ig it would be a good idea, in off hand we can make the pinch like as we do for volume control for keeping the speed and we can move hand left right, up down for rotation. it will be just keep rotating until the hand doesnt some in normal pose again. 
For these all  ig i will have to do something with vector estimation kinda thingy. imma cmplete linear algebra fast and practise it lil bit.
we will be doing the pinch thingy in off hand for sensitivity and far means more and close means less. and the other fingers must be warped so as to it will be differ than keeping hand in rest.

Btw we can also do rotation through hand pointing through a finger at direction, that would be easier (and might be better). Lets firstly try upper one then this will be as second option,,

-----------

till now we implemented the palm orientation detection only, here's how:

1st try: as i did in main.py, i set the rest pose byt  thumb up from off hand then i check if len of hand landmark if more than 0 and rest pose exists, then i get pinky and wrist finger's current value  and rest_pose_value. i create a var for pinky and wrist diff and subtract current z value of that ldm from rest value z value to get get the diff. then by sme trial and err i check if its between some values so top/bottom or else left/right. though it had 1 mmajor drawback: it wasn't that accurate ngl, sometime wrist diff tells correct fr top bottom but sometimes it caalcullated for left right and vice versa for pinky... i also tried using other ldm like middle finger mcp, but it wasn't that accurate at all..

2nd try: so i had this idea like what if we get a line start from pinky to the wrist and we find its top perpendicular line then we can see its direction vector and figure out the rotation byt try andd err. i created a direction vector first from wrist to pinky through subtracting coords then i saw this formula to rotate line  90deg: (-dy, dx) in left side.
i made perpendicular_ldm_left(a normalized ldm), then put this new values(-dy,dx) as x,y and found the average z. then i appended it in rest pose then in tools.py, made some changed to visualize this dot. ot was smthing working better visually but it wasn;t that accurate too.

thats when i got [this](https://stackoverflow.com/questions/72003980/can-we-get-the-orientation-of-the-hand-from-mediapipes-palm-detector), it was exactly what i wanted(though had some mistakes like subtracting NormalizedLandmark using numpy rather extracting coords in list etc etc):it uses world landmarks instead of simple hand ldm, it creates a numpy array of 3 ldms: wrist, index mcp, and pinky mcp(to create a plain that cvrs the palm), then from those points, it makes 2 direction vectors: from wrist to pinky and pinky to inde. then it finds the cross product of these dir vectors(that lies in our plain), and the cross producct return a normal vector perpendicular to both dir vectors and we normalize it to be a unit vector(length 1), then create a new NormalizedLandmark and assign the values as we got then append in rest_pose for visualizing and using if-else for finding right/left and up/down, and surprisingly, it ws much more stable and accurate!

Though in future i might use all MCPs for better result. and since different user might keep their hand differently, in future we shouldcan select and set values in beginning in future.

-----------

So i tried implementing the palm orientation detection in gesture_mapper, but it was misperforming, and i realized that we were flipping the img in main.py in the beginning but i found it kind of awkward, i mean we were using it so that when user does something with right hand, it shows right hand in user perspective but due to this, i had to do the opposite config like i worte main hand as left so it chooses right etc. But in our experiment py file, we had written code for non flip ldm, so i ended up removing the logic to flip img in beginning and kept it in last to show to user only, and changed constants as mian hand is right and off hand is left.

Then i implemented the orien. detection code in gesture mapper and appended the up_rotate, down_rotate, left and right in mouse btn types, and in action taker, rn we are just printing like up rotate, down rotate etc. since we are using press and release approach, we will need to use seperate thread as we are doing for cps, i think i should share the thread.. will do it next!

-----------

So this took really lotta effort, here's what happened: So since beginning i wanted to share the thread with all. So at first i thought to use an array where i store all tasks that has to be performed in parallel, but there was several problem like how on earth we can run all tasks in parallel in single thread when each task is a while loop, so we had to run in sequence but we didn't want it at all. So after shaking head for hrs, i found some common things in it: all(cps and 4 rotations) need to run in while loop and have a sleep(nearly 0.15 for cps, and 0.01 for rotation). So instead of running while loop for all, what if in the task, i add a last_ran and sleep_interval property and we run while loop a single time since the class initiates and everytime checks if there are tasks, if yes then do for loop and see `if (current time - last ran) > sleep_interval`(it means if the time when task was ran last is older than sleep interval, execute the task again and last_ran must be current time). 
By this way we were running a single while loop in thread, every task has their own last_ran and sleep_interval, the thread checks elapsed time and if its larger than sleep interval, run it and change last_ran and continue this loop!

though it has a problem: we are running while loop everytime, and doing checks and we are doing it even though tasks are 0, this thing is cpu intensive that my fps drops from 20 to ~5.. We gotta solve it afap