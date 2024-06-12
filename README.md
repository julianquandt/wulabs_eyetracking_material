# Description

 	$${\color{red}Red}$$

$${\color{red}__Important note: This was developed for Psychopy Version 2024.1.4 but should also work with newer Versions. For older versions the routine might not work. You can best download Version 2024.1.4 for [Windows](https://github.com/psychopy/psychopy/releases/download/2024.1.4/StandalonePsychoPy-2024.1.4-win64.exe) or [MAC](https://github.com/psychopy/psychopy/releases/download/2024.1.4/StandalonePsychoPy-2024.1.4-macOS.dmg) to make sure this works as expected.__}$$

These are the materials that are necessary to run EyeTracking Experiments in WULABS.
The repository contains 2 folders and a powerpoint presentation.

The `eyetracker_calibrate_wulabs` folder contains an automatic calibration routine that explains eyetracking to participants.
Hopefully, by using this routine, most of the participants should be able to calibrate their eyetrackers without further help.
It contains some instruction images and a procedure that will try to calibrate the eyetracker. 
In case the calibration fails on the first try, participants will be asked to read the instructions again and retry the calibration.
In case the calibration fails a second time, participants are asked to contact the researcher for assistance.

The `psychopy_eyetracker_tobii` folder contains the technical implementation of the calibration routine.
It is an adjustment of the standard tobii calibration routine, that was visually improved. 

The powerpoint presentation is mainly there as an illustration of what the instruction screens look like (currently the instructions are only a beta version and are neither completely correct nor polished)

# Installation

To use the calibration routine yourself you have to follow two steps, which mainly contains moving the folders to the right places.

First, to download the folders, click [HERE](https://github.com/julianquandt/wulabs_eyetracking_material/archive/refs/heads/main.zip).
Once downloaded, extract the content and copy the folders as follows:

1. Copy the `eyetracker_calibrate_wulabs` folder to your psychopy directory.
   - For this, you need to find the Psychopy installation on your machine. To find out where it is, open the Psychopy Builder.
   - Click on `Help` in the menu and select `System Info...`
   - In the opened dialogue, search for `Python Info` and copy the part before the last \ (or / if you are on mac or linux)
   - Paste the path to your file explorer (or navigate there manually).
   - Once you are in this folder, navigate to `Lib > site-packages > psychopy > experiment > routines`.
   - Copy the `eyetracker_calibrate_wulabs` (the entire folder, not just the content) here.
2. Navigate back, until you are in the `site-packages` folder again.
   - Once you are in this folder, copy and paste the `psychopy_eyetracker_tobii` folder here.
   - You will probably be asked if you want to replace existing files. Select `Replace files`.

Restart Psychopy.
In the Builder, Psychopy should now show the new `Eyetracker Calibration WULABS` routine under the `Eyetracking` components on the right.

# Usage

Once the routine is available, you can basically use it like the standard eyetracking calibration routine, however there are a few differences:

1. You will not need to add a validation routine. The validation is already included in the WULABS calibration routine.
2. There are a few additional settings that can be set:
   - `Criterion for passing calibration`: This determines which criterion should be used for checking if the calibration succeeded. The standard setting is `max_error`, meaning that if the maximum deviation between the target and eye gaze is too high during validation, the calibration will count as failed and the routine will repeat. The alternative `mean_error` uses the average to determine the success of the calibration. Usually you do not want to change this unless you have good reason.
   - `Criterion for validation pass`: This is the value that is used for `max_error`or `mean_error` in screen units. Usually you do not want to change this unless you have good reason.
   - `attempts`: This is the total amount of attempts that someone will have at calibrating the eyetracker. For instance, 3 attempts means that the routine will try calibration 3 times, until no further attempts will be made, and it is assumed that for some reason (e.g. glasses) the participant is not eligable for eyetracking.
   - `Break after failed attempts`: This determines when the participant will be told to consult the experimenter. Currently set to 1, which confusingly means that it will happen after the _second_ attempt (python uses 0 for index and I haven't fixed this yet)

The rest is basically the same as for the regular eye tracking experiment.
After including this calibration, you can build your experiment as you are used to. 
