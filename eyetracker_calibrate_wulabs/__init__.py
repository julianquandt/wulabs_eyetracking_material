from .. import BaseStandaloneRoutine
from psychopy.localization import _translate
from psychopy.experiment import Param
from pathlib import Path
from psychopy.alerts import alert
import os



class EyetrackerCalibrationRoutineWULABS(BaseStandaloneRoutine):
    categories = ['Eyetracking']
    targets = ["PsychoPy"]
    iconFile = Path(__file__).parent / "eyetracker_calib.png"
    tooltip = _translate("Calibration routine for eyetrackers in WULABS")
    beta = True

    def __init__(self, exp, name='wulabs_calibration',
                 progressMode="time", targetDur=1.5, expandDur=1, expandScale=1.5,
                 movementAnimation=True, movementDur=1.0, targetDelay=1.0,
                 innerFillColor='green', innerBorderColor='black', innerBorderWidth=2, innerRadius=0.0035,
                 fillColor='', borderColor="black", borderWidth=2, outerRadius=0.01,
                 colorSpace="rgb", units='from exp settings',
                 targetLayout="NINE_POINTS", randomisePos=True, textColor='black', 
                 attempts = int(3), attemptBreak = int(1), passCriterion = "max_error", criterionValue = 0.2,
                 gaze_cursor = 'green', show_results_screen = False, save_results_screen = False,
                 disabled=False, 
                 instruction_pages=["instruction_page1", "instruction_page2", "instruction_page3", "instruction_page4", "instruction_page5", "instruction_page6","instruction_page7", "instruction_page8"],
                 instruction_path = Path(__file__).parent
                 ):
        # Initialise base routine
        BaseStandaloneRoutine.__init__(self, exp, name=name, disabled=disabled)
        self.url = "https://psychopy.org/builder/components/eyetracker_calibration.html"

        self.exp.requirePsychopyLibs(['iohub', 'hardware'])

        # Basic params
        self.order += [
            "targetLayout",
            "randomisePos",
            "textColor",
            "attempts",
            "attemptBreak",
            "passCriterion",
            "criteriaValue",
            "gaze_cursor",
            "show_results_screen",
            "save_results_screen",
            "instruction_pages",
            "instruction_path"
        ]

        del self.params['stopVal']
        del self.params['stopType']

        self.params['targetLayout'] = Param(targetLayout,
                                            valType='str', inputType="choice", categ='Basic',
                                            allowedVals=['THREE_POINTS', 'FIVE_POINTS', 'NINE_POINTS', "THIRTEEN_POINTS"],
                                            hint=_translate("Pre-defined target layouts"),
                                            label=_translate("Target layout"))

        self.params['randomisePos'] = Param(randomisePos,
                                            valType='bool', inputType="bool", categ='Basic',
                                            hint=_translate("Should the order of target positions be randomised?"),
                                            label=_translate("Randomise target positions"))
        self.params['textColor'] = Param(textColor,
                                     valType='color', inputType="color", categ='Basic',
                                     hint=_translate("Text foreground color"),
                                     label=_translate("Text color"))
        self.params['attempts'] = Param(int(attempts), 
                                        valType='num', inputType="single", categ='Basic',
                                           hint=_translate(
                                               "How many attempts should be done if the accuracy is not ok?."),
                                           label=_translate("attempts"))
        self.params['attemptBreak'] = Param(int(attemptBreak), valType='num', inputType="single", categ='Basic',
                                           hint=_translate(
                                               "After how many failed attempts should the Experimenter be called?."),
                                           label=_translate("Break after failed attempts"))
        self.params['passCriterion'] = Param(passCriterion, 
                                            valType='str', inputType="choice", categ='Basic',
                                            allowedVals=['mean_error', 'max_error'],
                                           label=_translate("Criterion for passing calibration"))
        self.params['criterionValue'] = Param(criterionValue, 
                                           valType='num', inputType="single", categ='Basic',
                                           hint=_translate(
                                               "At what criterion value should the validation be passed?."),
                                           label=_translate("criterion value of validation pass"))
        self.params['gaze_cursor'] = Param(gaze_cursor, 
                                           valType='color', inputType="color", categ='Basic',
                                        hint=_translate("Fill color of the gaze cursor in Calibration"),
                                        label=_translate("Gaze cursor color"))
        self.params['show_results_screen'] = Param(show_results_screen, 
                                         valType='bool', inputType="bool", categ='Basic',
                                            hint=_translate("Should the screen with validation results be shown?"),
                                            label=_translate("Show validation results screen"))
        self.params['save_results_screen'] = Param(save_results_screen, 
                                         valType='bool', inputType="bool", categ='Basic',
                                            hint=_translate("Should the screen with validation results be saved?"),
                                            label=_translate("Save validation results screen"))
        self.params['instruction_pages'] = Param(instruction_pages, valType='list', inputType="list", categ='Basic',
                                             hint=_translate("Instruction pages to show before calibration"),
                                             label=_translate("Instruction pages"))
        self.params['instruction_path'] = Param(instruction_path, valType='str', inputType="str", categ='Basic',
                                                hint=_translate("Path to the instruction pages"),
                                                label=_translate("Instruction path"))
        
        # Target Params
        self.order += [
            "targetStyle",
            "fillColor",
            "borderColor",
            "innerFillColor",
            "innerBorderColor",
            "colorSpace",
            "borderWidth",
            "innerBorderWidth",
            "outerRadius",
            "innerRadius"
        ]

        self.params['innerFillColor'] = Param(innerFillColor,
                                     valType='color', inputType="color", categ='Target',
                                     hint=_translate("Fill color of the inner part of the target"),
                                     label=_translate("Inner fill color"))

        self.params['innerBorderColor'] = Param(innerBorderColor,
                                           valType='color', inputType="color", categ='Target',
                                           hint=_translate("Border color of the inner part of the target"),
                                           label=_translate("Inner border color"))

        self.params['fillColor'] = Param(fillColor,
                                         valType='color', inputType="color", categ='Target',
                                         hint=_translate("Fill color of the outer part of the target"),
                                         label=_translate("Outer fill color"))

        self.params['borderColor'] = Param(borderColor,
                                           valType='color', inputType="color", categ='Target',
                                           hint=_translate("Border color of the outer part of the target"),
                                           label=_translate("Outer border color"))

        self.params['colorSpace'] = Param(colorSpace,
                                          valType='str', inputType="choice", categ='Target',
                                          allowedVals=['rgb', 'dkl', 'lms', 'hsv'],
                                          hint=_translate(
                                              "In what format (color space) have you specified the colors? (rgb, dkl, lms, hsv)"),
                                          label=_translate("Color space"))

        self.params['borderWidth'] = Param(borderWidth,
                                           valType='num', inputType="single", categ='Target',
                                           hint=_translate("Width of the line around the outer part of the target"),
                                           label=_translate("Outer border width"))

        self.params['innerBorderWidth'] = Param(innerBorderWidth,
                                           valType='num', inputType="single", categ='Target',
                                           hint=_translate("Width of the line around the inner part of the target"),
                                           label=_translate("Inner border width"))

        self.params['outerRadius'] = Param(outerRadius,
                                           valType='num', inputType="single", categ='Target',
                                           hint=_translate("Size (radius) of the outer part of the target"),
                                           label=_translate("Outer radius"))

        self.params['innerRadius'] = Param(innerRadius,
                                           valType='num', inputType="single", categ='Target',
                                           hint=_translate("Size (radius) of the inner part of the target"),
                                           label=_translate("Inner radius"))

        self.params['units'] = Param(units,
                                     valType='str', inputType="choice", categ='Target',
                                     allowedVals=['from exp settings'], direct=False,
                                     hint=_translate("Units of dimensions for this stimulus"),
                                     label=_translate("Spatial units"))


        # Animation Params
        self.order += [
            "progressMode",
            "targetDur",
            "expandDur",
            "expandScale",
            "movementAnimation",
            "movementDur",
            "targetDelay"
        ]

        self.params['progressMode'] = Param(progressMode,
                                            valType="str", inputType="choice", categ="Animation",
                                            allowedVals=["space key", "time"],
                                            hint=_translate("Should the target move to the next position after a "
                                                            "keypress or after an amount of time?"),
                                            label=_translate("Progress mode"))

        self.depends.append(
            {"dependsOn": "progressMode",  # must be param name
             "condition": "in ['time', 'either']",  # val to check for
             "param": "targetDur",  # param property to alter
             "true": "show",  # what to do with param if condition is True
             "false": "hide",  # permitted: hide, show, enable, disable
             }
        )

        self.params['targetDur'] = Param(targetDur,
                                         valType='num', inputType="single", categ='Animation',
                                         hint=_translate(
                                             "Time limit (s) after which progress to next position"),
                                         label=_translate("Target duration"))

        self.depends.append(
            {"dependsOn": "progressMode",  # must be param name
             "condition": "in ['space key', 'either']",  # val to check for
             "param": "expandDur",  # param property to alter
             "true": "show",  # what to do with param if condition is True
             "false": "hide",  # permitted: hide, show, enable, disable
             }
        )

        self.params['expandDur'] = Param(expandDur,
                                         valType='num', inputType="single", categ='Animation',
                                         hint=_translate(
                                             "Duration of the target expand/contract animation"),
                                         label=_translate("Expand / contract duration"))

        self.params['expandScale'] = Param(expandScale,
                                           valType='num', inputType="single", categ='Animation',
                                           hint=_translate("How many times bigger than its size the target grows"),
                                           label=_translate("Expand scale"))

        self.params['movementAnimation'] = Param(movementAnimation,
                                                 valType='bool', inputType="bool", categ='Animation',
                                                 hint=_translate(
                                                     "Enable / disable animations as target stim changes position"),
                                                 label=_translate("Animate position changes"))

        self.depends.append(
            {"dependsOn": "movementAnimation",  # must be param name
             "condition": "== True",  # val to check for
             "param": "movementDur",  # param property to alter
             "true": "show",  # what to do with param if condition is True
             "false": "hide",  # permitted: hide, show, enable, disable
             }
        )

        self.params['movementDur'] = Param(movementDur,
                                           valType='num', inputType="single", categ='Animation',
                                           hint=_translate(
                                               "Duration of the animation during position changes."),
                                           label=_translate("Movement duration"))

        self.depends.append(
            {"dependsOn": "movementAnimation",  # must be param name
             "condition": "== False",  # val to check for
             "param": "targetDelay",  # param property to alter
             "true": "show",  # what to do with param if condition is True
             "false": "hide",  # permitted: hide, show, enable, disable
             }
        )

        self.params['targetDelay'] = Param(targetDelay,
                                           valType='num', inputType="single", categ='Animation',
                                           hint=_translate(
                                               "Duration of the delay between positions."),
                                           label=_translate("Target delay"))

    def writeMainCode(self, buff):
        # Alert user if eyetracking isn't setup
        if self.exp.eyetracking == "None":
            alert(code=4505)
        # Get inits
        inits = self.params
        # Code-ify 'from exp settings'
        if self.params['units'].val == 'from exp settings':
            inits['units'].val = None
        # Synonymise expand dur and target dur
        if inits['progressMode'].val == 'time':
            inits['expandDur'] = inits['targetDur']
        if inits['progressMode'].val == 'space key':
            inits['targetDur'] = inits['expandDur']
        # Synonymise movement dur and target delay
        if inits['movementAnimation'].val:
            inits['targetDelay'] = inits['movementDur']
        else:
            inits['movementDur'] = inits['targetDelay']

        attempts_int = int(inits['attempts'].val)


        # create paths to instruction pages pointing to current parent dir
        instruction_pages = inits['instruction_pages'].val

        # for builder compatability, first make instruction_pages a string and strip any list characters, then convert back to list
        instruction_pages = str(instruction_pages).strip('[]')
        # check if instruction_pages is list and convert to list if not
        if not isinstance(instruction_pages, list):
            instruction_pages = [item.strip().strip("'") for item in instruction_pages.split(",")]
        
        instruction_paths = [os.path.join(inits['instruction_path'].val, f"{page}.png") for page in instruction_pages]

        inits['instruction_pages'].val = instruction_paths

        BaseStandaloneRoutine.writeMainCode(self, buff)

        # initiate loop for each repetition
        # Make calibration target
        code = (
            "# define target for %(name)s\n"
            "%(name)sTarget = visual.TargetStim(win, \n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
                "name='%(name)sTarget',\n"
                "radius=%(outerRadius)s, fillColor=%(fillColor)s, borderColor=%(borderColor)s, lineWidth=%(borderWidth)s,\n"
                "innerRadius=%(innerRadius)s, innerFillColor=%(innerFillColor)s, innerBorderColor=%(innerBorderColor)s, innerLineWidth=%(innerBorderWidth)s,\n"
                "colorSpace=%(colorSpace)s, units=%(units)s\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = (
            ")"
        )
        buff.writeIndentedLines(code % inits)
        # Make config object
        code = (
            "# define parameters for %(name)s\n"
            "%(name)s = hardware.eyetracker.EyetrackerCalibration(win, \n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
                "eyetracker, %(name)sTarget,\n"
                "units=%(units)s, colorSpace=%(colorSpace)s,\n"
                "progressMode=%(progressMode)s, targetDur=%(targetDur)s, expandScale=%(expandScale)s,\n"
                "targetLayout=%(targetLayout)s, randomisePos=%(randomisePos)s, textColor=%(textColor)s,\n"
                "movementAnimation=%(movementAnimation)s, targetDelay=%(targetDelay)s\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = (
            ")\n"
        )
        buff.writeIndentedLines(code % inits)
        # Make validation target
        code = (
            "# define target for %(name)s\n"
            "%(name)sValidationTarget = visual.TargetStim(win, \n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
                "name='%(name)sValidationTarget',\n"
                "radius=%(outerRadius)s, fillColor=%(fillColor)s, borderColor=%(borderColor)s, lineWidth=%(borderWidth)s,\n"
                "innerRadius=%(innerRadius)s, innerFillColor=%(innerFillColor)s, innerBorderColor=%(innerBorderColor)s, innerLineWidth=%(innerBorderWidth)s,\n"
                "colorSpace=%(colorSpace)s, units=%(units)s\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = (
            ")"
        )
        buff.writeIndentedLines(code % inits)
        # Make config object
        code = (
            "# define parameters for %(name)s\n"
            "%(name)sValidation = iohub.ValidationProcedure(win, \n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
                "target= %(name)sValidationTarget,\n"
                "gaze_cursor= %(gaze_cursor)s, positions=%(targetLayout)s, randomize_positions=%(randomisePos)s,\n"
                "expand_scale=%(expandScale)s, target_duration=%(targetDur)s, enable_position_animation=%(movementAnimation)s,\n"
                "target_delay=%(targetDelay)s, progress_on_key=None, text_color=%(textColor)s,\n"
                "show_results_screen=%(show_results_screen)s, save_results_screen=%(save_results_screen)s, \n"
                "unit_type=%(units)s, color_space=%(colorSpace)s\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = (
            ")\n"
        )
        buff.writeIndentedLines(code)
        code = (
            "%s%s%s" % ("for i in range(", attempts_int, "):\n")
        )
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
         # show instruction pages and allow to go back and forth betwen them
        code = (
            "# show instructions and allow to go back and forth betwen them\n"
            "instrPages = %(instruction_pages)s\n"
            "nPages = len(instrPages)\n"
            "nPage = 0\n"
            "while nPage < nPages:\n")
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
            "instr = visual.ImageStim(win, image=instrPages[nPage], units='norm', size=(2, 2))\n"
            "instr.draw()\n"
            "win.flip()\n"
        )
        # new part for last page is space

        buff.writeIndentedLines(code % inits)
        code = (
            "if nPage == nPages - 1:\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
            "resp = event.waitKeys(keyList=['c', 'left'])\n"
            "if resp[0] == 'c':\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
            "nPage += 1\n"
            "event.clearEvents()\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = (
            "elif resp[0] == 'left':\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
            "nPage -= 1\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-2, relative=True)
        code = (
            "else:\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
            "resp = event.waitKeys(keyList=['left', 'right'])\n"
            "if resp[0] == 'left':\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
            "if nPage > 0:\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
            "nPage -= 1\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-2, relative=True)
        code = (
            "else:\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
            "nPage += 1\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-3, relative=True)

        # start calibration
        code = (
            "# run calibration\n"
            "%(name)s.run()\n"
            "# clear any keypresses from during %(name)s so they don't interfere with the experiment\n"
            "defaultKeyboard.clearEvents()\n"
        )
        buff.writeIndentedLines(code % inits)
        code = (
            "# run validation\n"
            "validation_results = %(name)sValidation.run()\n"
            "validation_criterion = validation_results[%(passCriterion)s]\n"
            "if validation_criterion <= %(criterionValue)s:\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
            "# calibration passed\n"
            "msg = 'The calibration was successfull. Please keep your head in the current position and press C to continue to the experiment.'\n"
            "detailed_instructions = visual.TextStim(win, \n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
            "text=msg, color=%(textColor)s, units='norm', colorSpace=%(colorSpace)s,\n"
            "pos=(0, 0), height=0.05, wrapWidth=1.5\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = (
            ")\n"
            "detailed_instructions.draw()\n"
            "win.flip()\n"
            "event.waitKeys(keyList=['c'])\n"
            "break\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = (
            "# calibration failed\n"
            "else:\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
            "if i == 0:\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
            "# first attempt failed\n"
            "msg = 'Calibration failed. Please repeat the calibration process.'\n"
            "detailed_instructions = visual.TextStim(win, \n"
            )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
                "text=msg, color=%(textColor)s, units='norm', colorSpace=%(colorSpace)s,\n"
                "pos=(0, 0), height=0.05, wrapWidth=1.5\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = (
            ")\n"
            "detailed_instructions.draw()\n"
            "win.flip()\n"
            "event.waitKeys(keyList=['c'])\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = (
            "elif i == %(attemptBreak)s:\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
            "# last attempt failed\n"
            "msg = 'Calibration failed again. Please Raise your arm to contact the experimenter.'\n"
            "detailed_instructions = visual.TextStim(win, \n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
            "text=msg, color=%(textColor)s, units='norm', colorSpace=%(colorSpace)s,\n"
            "pos=(0, 0), height=0.05, wrapWidth=1.5\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = (
            ")\n"
            "detailed_instructions.draw()\n"
            "win.flip()\n"
            "event.waitKeys(keyList=['s'])\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-2, relative=True)
        code = (
            "# clear any keypresses from during %(name)sValidation so they don't interfere with the experiment\n"
            "defaultKeyboard.clearEvents()\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
