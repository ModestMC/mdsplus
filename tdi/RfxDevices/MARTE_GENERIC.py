# -*- coding: iso-8859-1 -*-
from MDSplus import mdsExceptions, Device, Tree, Data, Event
from os import environ
from time import sleep

class MARTE_GENERIC(Device):
    """MARTe configuration"""
    parts=[{'path':':COMMENT', 'type':'text'},
      {'path':':ID', 'type':'numeric', 'value':0},
      {'path':':FREQUENCY', 'type':'numeric'},
      {'path':':TRIG_SOURCE', 'type':'numeric'},
      {'path':':DURATION', 'type':'numeric'},
      {'path':':OFFSET_START', 'type':'numeric', 'value':-1.},
      {'path':':OFFSET_END', 'type':'numeric', 'value':0.},
      {'path':':SAMPL_START', 'type':'numeric', 'value':0},
      {'path':':SAMPL_END', 'type':'numeric', 'value':0.5},
      {'path':':INPUT_CAL', 'type':'numeric', 'value':Data.execute('replicate([1.,0.],0,192)')},
      {'path':':OUTPUT_CAL', 'type':'numeric', 'value':Data.execute('replicate([1.,0.],0,192)')},
      {'path':':CONTROL', 'type':'text', 'value':'NONE'}]
#      {'path':'.PARAMS', 'type':'structure'},
#      {'path':'.PARAMS:NUM_ACTIVE', 'type':'numeric', 'value':0}]
#    for i in range(256):
#      parts.append({'path':'.PARAMS:PAR_%03d'%(i+1), 'type':'structure'})
#      parts.append({'path':'.PARAMS:PAR_%03d:DESCRIPTION'%(i+1), 'type':'text'})
#      parts.append({'path':'.PARAMS:PAR_%03d:NAME'%(i+1), 'type':'text'})
#      parts.append({'path':'.PARAMS:PAR_%03d:TYPE'%(i+1), 'type':'text'})
#      parts.append({'path':'.PARAMS:PAR_%03d:DIMS'%(i+1), 'type':'numeric'})
#      parts.append({'path':'.PARAMS:PAR_%03d:DATA'%(i+1), 'type':'numeric'})

#    parts.append({'path':'.WAVE_PARAMS', 'type':'structure'})
#    parts.append({'path':'.WAVE_PARAMS:NUM_ACTIVE', 'type':'numeric', 'value':0})
#    for i in range(64):
#      parts.append({'path':'.WAVE_PARAMS:WAVE_%03d'%(i+1), 'type':'structure'})
#      parts.append({'path':'.WAVE_PARAMS:WAVE_%03d:DESCRIPTION'%(i+1), 'type':'text'})
#      parts.append({'path':'.WAVE_PARAMS:WAVE_%03d:NAME'%(i+1), 'type':'text'})
#      parts.append({'path':'.WAVE_PARAMS:WAVE_%03d:X'%(i+1), 'type':'numeric'})
#      parts.append({'path':'.WAVE_PARAMS:WAVE_%03d:Y'%(i+1), 'type':'numeric'})

    parts.append({'path':'.SIGNALS', 'type':'structure'})
    parts.append({'path':'.SIGNALS.ADC_IN', 'type':'structure'})
    for i in range(192):
      parts.append({'path':'.SIGNALS.ADC_IN:ADC_IN_%03d'%(i+1), 'type':'signal'})
    parts.append({'path':'.SIGNALS.DAC_OUT', 'type':'structure'})
    for i in range(96):
      parts.append({'path':'.SIGNALS.DAC_OUT:DAC_OUT_%03d'%(i+1), 'type':'signal'})
    parts.append({'path':'.SIGNALS.USER', 'type':'structure'})
    parts.append({'path':'.SIGNALS.USER:NAMES', 'type':'text'})
    for i in range(256):
      parts.append({'path':'.SIGNALS.USER.USER_%03d'%(i+1), 'type':'structure'})
      parts.append({'path':'.SIGNALS.USER.USER_%03d:NAME'%(i+1), 'type':'text'})
      parts.append({'path':'.SIGNALS.USER.USER_%03d:DESCRIPTION'%(i+1), 'type':'text'})
      parts.append({'path':'.SIGNALS.USER.USER_%03d:DATA'%(i+1), 'type':'signal'})
    parts.append({'path':':INIT_ACTION','type':'action',
	  'valueExpr':"Action(Dispatch('CPCI_SERVER','SEQ_INIT',50,None),Method(None,'init',head))",
	  'options':('no_write_shot',)})
    parts.append({'path':':STORE_ACTION','type':'action',
	  'valueExpr':"Action(Dispatch('MARTE_SERVER','SEQ_STORE',50,None),Method(None,'store',head))",
	  'options':('no_write_shot',)})
    del(i)

    def getEventName(self):
      if environ.get("MARTE_EVENT") is None:
        return "MARTE"
      else:
        return environ["MARTE_EVENT"]

    def init(self,*arg):
      eventStr = "SETUP " + str(self.id.data()) + " " + Tree.getActiveTree().name
      eventStr = eventStr + " " + str(Tree.getActiveTree().shot)
      try:
        eventStr = eventStr + " " + str(self.frequency.data())
      except:
        Data.execute('DevLogErr($1,$2)', self.nid, 'Cannot read frequency')
        return mdsExceptions.TclFAILED_ESSENTIAL.status
      try:
        eventStr = eventStr + " " + str(self.trig_source.data())
      except:
        Data.execute('DevLogErr($1,$2)', self.nid, 'Cannot read trigger source')
        return mdsExceptions.TclFAILED_ESSENTIAL.status
      try:
        eventStr = eventStr + " " + str(self.sampl_start.data())
      except:
        Data.execute('DevLogErr($1,$2)', self.nid, 'Cannot read Sampling start')
        return mdsExceptions.TclFAILED_ESSENTIAL.status
      try:
        eventStr = eventStr + " " + str(self.sampl_end.data())
      except:
        Data.execute('DevLogErr($1,$2)', self.nid, 'Cannot read Sampling end')
        return mdsExceptions.TclFAILED_ESSENTIAL.status
      try:
        eventStr = eventStr + " " + str(self.offset_start.data())
      except:
        Data.execute('DevLogErr($1,$2)', self.nid, 'Cannot read Offset start')
        return mdsExceptions.TclFAILED_ESSENTIAL.status
      try:
        eventStr = eventStr + " " + str(self.offset_end.data())
      except:
        Data.execute('DevLogErr($1,$2)', self.nid, 'Cannot read Offset end')
        return mdsExceptions.TclFAILED_ESSENTIAL.status
      try:
        eventStr = eventStr + " " + str(self.duration.data())
      except:
        Data.execute('DevLogErr($1,$2)', self.nid, 'Cannot read Duration')
        return mdsExceptions.TclFAILED_ESSENTIAL.status

      eventStr = eventStr + " " + str(self.params.getNid())
      eventStr = eventStr + " " + str(self.wave_params.getNid())
      eventStr = eventStr + " " + str(self.input_cal.getNid())
      eventStr = eventStr + " " + str(self.output_cal.getNid())
      try:
        eventStr = eventStr + " " + self.control.data()
      except:
        Data.execute('DevLogErr($1,$2)', self.nid, 'Cannot read Control')
        return mdsExceptions.TclFAILED_ESSENTIAL.status
      eventStr = eventStr + " " + str(self.signals_adc_in.getNid())
      eventStr = eventStr + " " + str(self.signals_dac_out.getNid())
      eventStr = eventStr + " " + str(self.signals_user.getNid())
      print(eventStr)
      Event.setevent(self.getEventName(), eventStr)
      sleep(3)
      return 1


    def trigger(self,*arg):
      eventStr = "TRIGGER " + str(self.id.data())
      Event.setevent(self.getEventName(), eventStr)
      return 1

    def pre_req(self,*arg):
      eventStr = "PRE_REQ " + str(self.id.data())
      Event.setevent(self.getEventName(), eventStr)
      return 1

    def pulse_req(self,*arg):
      eventStr = "PULSE_REQ"
      Event.setevent(self.getEventName(), eventStr)
      return 1

    def post_req(self,*arg):
      eventStr = "POST_REQ"
      Event.setevent(self.getEventName(), eventStr)
      return 1

    def collection_complete(self,*arg):
      eventStr = "COLLECTION_COMPLETE"
      Event.setevent(self.getEventName(), eventStr)
      return 1

    def store(self,*arg):
      eventStr = "STORE " + str(self.id.data())
      eventStr = eventStr + " " + str(self.signals_adc_in.getNid())
      eventStr = eventStr + " " + str(self.signals_dac_out.getNid())
      eventStr = eventStr + " " + str(self.signals_user.getNid())
      Event.setevent("MARTE", eventStr)
      sleep(3)
      return 1

    def abort(self,*arg):
      eventStr = "ABORT"
      Event.setevent(self.getEventName(), eventStr)
      return 1

    def cacca(self,*arg):
      eventStr = "COLLECTION_COMPLETE"
      Event.setevent(self.getEventName(), eventStr)
      return 1
#       eventStr = "STORE " +str(self.id.data())
#       print eventStr
#       Event.setevent(self.getEventName(), eventStr)
#       sleep(10)
#       return 1

    def seq_init(self,*arg):
      self.abort()
      sleep(3)
      self.pre_req()
      sleep(3)
      self.init()
      self.pulse_req()
      return 1

    def seq_init_start(self,*arg):
      self.abort()
      sleep(3)
      self.pre_req()
      sleep(3)
      self.init()
      return 1

    def seq_init_stop(self,*arg):
      self.init()
      self.pulse_req()
      return 1

    def seq_store(self,*arg):
      self.post_req()
      sleep(3)
      self.store()
      sleep(3)
      self.collection_complete()
      return 1

    def seq_store_start(self,*arg):
      self.post_req()
      sleep(3)
      self.store(ag)
      return 1

    def seq_store_stop(self,*arg):
      self.store()
      self.collection_complete()
      return 1
