# -*- coding: utf-8 -*-
# Part of the PsychoPy library
# Copyright (C) 2012-2020 iSolver Software Solutions (C) 2021 Open Science Tools Ltd.
# Distributed under the terms of the GNU General Public License (GPL).

from psychopy.iohub.devices.eyetracker.calibration import BaseCalibrationProcedure
from collections import OrderedDict
from psychopy import visual
from psychopy.iohub.constants import EventConstants
import gevent
from pathlib import Path
from psychopy import prefs
from psychopy.tools.monitorunittools import posToPix
import math


this_module_path = Path(__file__).parent




class TobiiCalibrationProcedure(BaseCalibrationProcedure):
    def __init__(self, eyetrackerInterface, calibration_args):
        self.feedback_resources = OrderedDict()
        self.feedback_resources_face = OrderedDict()
        self.feedback_texts = OrderedDict()
        self.facemask = OrderedDict()
        self.tobii_calibration = None
        self.cal_result_dict = dict(status="Calibration Not Started")
        BaseCalibrationProcedure.__init__(self, eyetrackerInterface, calibration_args, allow_escape_in_progress=True)

    def createGraphics(self):
        """
        """
        BaseCalibrationProcedure.createGraphics(self)

        # create Tobii eye position feedback graphics
        #
        sw, sh = self.screenSize
        self.hbox_bar_length = hbox_bar_length = sw / 4
        hbox_bar_height = 6
        marker_diameter = 7
        self.marker_heights = (-sh / 2.0 * .7, -sh / 2.0 * .75, -sh /
                               2.0 * .8, -sh / 2.0 * .7, -sh / 2.0 * .75, -sh / 2.0 * .8)

        bar_vertices = ([-hbox_bar_length / 2, -hbox_bar_height / 2], [hbox_bar_length / 2, -hbox_bar_height / 2],
                        [hbox_bar_length / 2, hbox_bar_height / 2], [-hbox_bar_length / 2, hbox_bar_height / 2])



        self.feedback_texts['feedback_txt_x'] = visual.TextStim(self.window, text="This one measures the X position",
                                            pos=(hbox_bar_length / 2 + 20, self.marker_heights[0]), height=20,
                                            color="red",
                                            units='pix', wrapWidth=self.width * 0.9)
        # self.feedback_texts['feedback_txt_y'] = visual.TextStim(self.window, text="This one measures the Y position",
        #                                     pos=(hbox_bar_length / 2 + 20, self.marker_heights[1]+10), height=20,
        #                                     color="red",
        #                                     units='pix', wrapWidth=self.width * 0.9),
        # self.feedback_texts['feedback_txt_z'] = visual.TextStim(self.window, text="This one measures the Z position",
        #                                     pos=(hbox_bar_length / 2 + 20, self.marker_heights[2]+10), height=20,
        #                                     color="red",
        #                                     units='pix', wrapWidth=self.width * 0.9),

        self.facemask['base'] = visual.ImageStim(self.window, image=this_module_path / 'facemask.png', units='pix', pos=(0, 0))
        self.facemask_eye_pos_left = [self.facemask['base'].pos[0]-90,self.facemask['base'].pos[1]+27]
        self.facemask_eye_pos_right = [self.facemask['base'].pos[0]+90, self.facemask['base'].pos[1]+27]


        self.facemask['live'] = visual.ImageStim(self.window, image=this_module_path / 'facemask.png', units='pix', pos=(0, 0), color = [1,0,0])



        # self.marker_heights_face = c(self.facemask['base'].pos[0]-90,self.facemask['base'].pos[1]+27, # x left eye
        #  )



        # facemask_eye_pos_left = [self.facemask['base'].pos[0]-(0.18*self.facemask['base'].size[0]),self.facemask['base'].pos[1]-(0.071*self.facemask['base'].size[1])]
        # facemask_eye_pos_right = [self.facemask['base'].pos[0]+(0.18*self.facemask['base'].size[1]), self.facemask['base'].pos[1]-(0.071*self.facemask['base'].size[1])]
        self.feedback_resources['hbox_bar_x'] = visual.ShapeStim(
            win=self.window,
            lineColor='White',
            fillColor='Firebrick',
            vertices=bar_vertices,
            units='pix',
            pos=(
                0,
                self.marker_heights[0]))
        self.feedback_resources['hbox_bar_y'] = visual.ShapeStim(
            win=self.window,
            lineColor='White',
            fillColor='DarkSlateGray',
            vertices=bar_vertices,
            units='pix',
            pos=(
                0,
                self.marker_heights[1]))
        self.feedback_resources['hbox_bar_z'] = visual.ShapeStim(
            win=self.window,
            lineColor='White',
            fillColor='GoldenRod',
            vertices=bar_vertices,
            units='pix',
            pos=(
                0,
                self.marker_heights[2]))

        marker_vertices = [-marker_diameter, 0], [0, marker_diameter], [marker_diameter, 0], [0, -marker_diameter]
        marker_vertices_face = [-marker_diameter, 0], [0, marker_diameter], [marker_diameter, 0], [0, -marker_diameter]
        self.feedback_resources['left_hbox_marker_x'] = visual.ShapeStim(
            win=self.window,
            lineColor='White',
            fillColor='Black',
            vertices=marker_vertices,
            units='pix',
            pos=(
                0,
                self.marker_heights[0]))
        self.feedback_resources['left_hbox_marker_y'] = visual.ShapeStim(
            win=self.window,
            lineColor='White',
            fillColor='Black',
            units='pix',
            vertices=marker_vertices,
            pos=(
                0,
                self.marker_heights[1]))
        self.feedback_resources['left_hbox_marker_z'] = visual.ShapeStim(
            win=self.window,
            lineColor='White',
            fillColor='Black',
            units='pix',
            vertices=marker_vertices,
            pos=(
                0,
                self.marker_heights[2]))
        self.feedback_resources['right_hbox_marker_x'] = visual.ShapeStim(
            win=self.window,
            lineColor='White',
            fillColor='DimGray',
            units='pix',
            vertices=marker_vertices,
            pos=(
                0,
                self.marker_heights[0]))
        self.feedback_resources['right_hbox_marker_y'] = visual.ShapeStim(
            win=self.window,
            lineColor='White',
            fillColor='DimGray',
            units='pix',
            vertices=marker_vertices,
            pos=(
                0,
                self.marker_heights[1]))
        self.feedback_resources['right_hbox_marker_z'] = visual.ShapeStim(
            win=self.window,
            lineColor='White',
            fillColor='DimGray',
            units='pix',
            vertices=marker_vertices,
            pos=(
                0,
                self.marker_heights[2]))
        

        self.feedback_resources_face['left_hbox_marker_x_face'] = visual.ShapeStim(
            win=self.window,
            lineColor='White',
            fillColor='Red',
            vertices=marker_vertices_face,
            units='pix',
            pos=(
                0,
                self.marker_heights[0]))
        self.feedback_resources_face['left_hbox_marker_y_face'] = visual.ShapeStim(
            win=self.window,
            lineColor='White',
            fillColor='Black',
            units='pix',
            vertices=marker_vertices_face,
            pos=(
                0,
                self.marker_heights[1]))
        self.feedback_resources_face['left_hbox_marker_z_face'] = visual.ShapeStim(
            win=self.window,
            lineColor='White',
            fillColor='Black',
            units='pix',
            vertices=marker_vertices_face,
            pos=(
                0,
                self.marker_heights[2]))
        self.feedback_resources_face['right_hbox_marker_x_face'] = visual.ShapeStim(
            win=self.window,
            lineColor='White',
            fillColor='Green',
            units='pix',
            vertices=marker_vertices_face,
            pos=(
                0,
                self.marker_heights[0]))
        self.feedback_resources_face['right_hbox_marker_y_face'] = visual.ShapeStim(
            win=self.window,
            lineColor='White',
            fillColor='DimGray',
            units='pix',
            vertices=marker_vertices_face,
            pos=(
                0,
                self.marker_heights[1]))
        self.feedback_resources_face['right_hbox_marker_z_face'] = visual.ShapeStim(
            win=self.window,
            lineColor='White',
            fillColor='DimGray',
            units='pix',
            vertices=marker_vertices_face,
            pos=(
                0,
                self.marker_heights[2]))


    def getHeadBoxPosition(self, events):
        # KeyboardInputEvent.CLASS_ATTRIBUTE_NAMES.index('key_id')
        left_eye_cam_x = None
        left_eye_cam_y = None
        left_eye_cam_z = None
        right_eye_cam_x = None
        right_eye_cam_y = None
        right_eye_cam_z = None

        if len(events) == 0:
            return (left_eye_cam_x, left_eye_cam_y, left_eye_cam_z), (right_eye_cam_x, right_eye_cam_y, right_eye_cam_z)

        event = events[-1]
        if abs(event.left_eye_cam_x) != 1.0 and abs(event.left_eye_cam_y) != 1.0:
            left_eye_cam_x = 1.0 - event.left_eye_cam_x
            left_eye_cam_y = event.left_eye_cam_y
        if event.left_eye_cam_z != 0.0:
            left_eye_cam_z = event.left_eye_cam_z
        if abs(event.right_eye_cam_x) != 1.0 and abs(event.right_eye_cam_y) != 1.0:
            right_eye_cam_x = 1.0 - event.right_eye_cam_x
            right_eye_cam_y = event.right_eye_cam_y
        if event.right_eye_cam_z != 0.0:
            right_eye_cam_z = event.right_eye_cam_z
        return (left_eye_cam_x, left_eye_cam_y, left_eye_cam_z), (right_eye_cam_x, right_eye_cam_y, right_eye_cam_z)

    def showIntroScreen(self, text_msg='Align the blue face with the black face by moving your head until the screen background turns green. \n Press SPACE to continue.'):
        self.clearAllEventBuffers()
        self._eyetracker.setRecordingState(True)

        orig_wincolor = self.window.color

        while True:
            self.textLineStim.setText(text_msg)
            
            # move the text to lower edge of the screen
            self.textLineStim.pos = (0, -self.window.size[1] / 2 + 50)
            event_named_tuples = []
            for e in self._eyetracker.getEvents(EventConstants.BINOCULAR_EYE_SAMPLE):
                event_named_tuples.append(
                    EventConstants.getClass(EventConstants.BINOCULAR_EYE_SAMPLE).createEventAsNamedTuple(e))
            leye_box_pos, reye_box_pos = self.getHeadBoxPosition(event_named_tuples)
            lx, ly, lz = leye_box_pos
            rx, ry, rz = reye_box_pos
            eye_positions = (lx, ly, lz, rx, ry, rz)
            marker_names = (
                'left_hbox_marker_x',
                'left_hbox_marker_y',
                'left_hbox_marker_z',
                'right_hbox_marker_x',
                'right_hbox_marker_y',
                'right_hbox_marker_z')
            # empty array of 6 elements
            pos_face = [float('nan')] * 6
            marker_heights = self.marker_heights
            hbox_bar_length = self.hbox_bar_length

            
            for i, p in enumerate(eye_positions):
                if p is not None:
                    mpoint = hbox_bar_length * p - hbox_bar_length / 2.0, marker_heights[i]

                    self.feedback_resources[marker_names[i]].setPos(mpoint)
                    if i in [0,3]: # adjust x_left positions
                        pos_face[i] = self.facemask['base'].size[0] *p - self.facemask['base'].size[0] / 2.0
                    elif i in [1,4]: # adjust y positions
                        pos_face[i] = self.facemask['base'].size[1]*p - self.facemask['base'].size[1]/2.0 
                    elif i in [2, 5]:
                        pos_face[i] = 1/(p/0.5)

            if not(math.isnan(pos_face[0]) or math.isnan(pos_face[3]) or math.isnan(pos_face[1]) or math.isnan(pos_face[4])):
                face_pos_x = (pos_face[0] + pos_face[3])
                face_pos_y = (pos_face[4] + pos_face[1])/2
                face_pos_coord = face_pos_x, -face_pos_y
                self.facemask['live'].setPos(face_pos_coord)
            if not(math.isnan(pos_face[2]) or math.isnan(pos_face[5])):
                print(pos_face[2], pos_face[5])
                scale_face_z = (pos_face[5] + pos_face[2])/2*self.facemask['base'].size[0], (pos_face[5] + pos_face[2])/2*self.facemask['base'].size[1]
                self.facemask['live'].size = scale_face_z

            if not(math.isnan(pos_face[0]) or math.isnan(pos_face[3]) or math.isnan(pos_face[1]) or math.isnan(pos_face[4])):
                # if the base and live mask align position and size-wise
                if (abs(self.facemask['base'].pos[0] - self.facemask['live'].pos[0]) < 20 and abs(self.facemask['base'].pos[1] - self.facemask['live'].pos[1]) < 20 and abs(self.facemask['base'].size[0] - self.facemask['live'].size[0]) < 20 and abs(self.facemask['base'].size[1] - self.facemask['live'].size[1]) < 20):
                    self.facemask['live'].color = [1,0,1]
                    self.window.color = [0.25,0.86,0.56]
                else:
                    self.facemask['live'].color = [1,0,0]
                    self.window.color = orig_wincolor

            self.facemask['base'].draw()

            self.facemask['live'].draw()
            # [r.draw() for r in self.feedback_resources.values()]


            self.textLineStim.draw()


            self.window.flip()

            msg = self.getNextMsg()
            if msg == 'SPACE_KEY_ACTION':
                self._eyetracker.setRecordingState(False)
                self.clearAllEventBuffers()
                self.window.color = orig_wincolor
                return True
            elif msg == 'QUIT':
                self._eyetracker.setRecordingState(False)
                self.clearAllEventBuffers()
                return False
            self.MsgPump()
            gevent.sleep()

    def startCalibrationHook(self):
        self.tobii_calibration = self._eyetracker._tobii.newScreenCalibration()
        self.tobii_calibration.enter_calibration_mode()

    def registerCalibrationPointHook(self, pt):
        self.tobii_calibration.collect_data(pt[0], pt[1])

    def finishCalibrationHook(self, aborted=False):
        cal_result_dict = dict(status="Calibration Aborted")
        if not aborted:
            calibration_result = self.tobii_calibration.compute_and_apply()
            cal_result_dict = dict(status=calibration_result.status)
            cal_result_dict['points'] = []
            for cp in calibration_result.calibration_points:
                csamples = []
                for cs in cp.calibration_samples:
                    csamples.append((cs.left_eye.position_on_display_area, cs.left_eye.validity))
                cal_result_dict['points'].append((cp.position_on_display_area, csamples))

        self.tobii_calibration.leave_calibration_mode()
        self.tobii_calibration = None
        self.cal_result_dict = cal_result_dict
