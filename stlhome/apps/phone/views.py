from django.shortcuts import redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from twilio.twiml import Response
from django_twilio.decorators import twilio_view

from stlhome.apps.shelters.models import Shelter
from stlhome.lib.twilioview import TwilioView
from stlhome.lib.twilioclient import client

from .models import Call

class StartView(TwilioView):
    def get(self, request):
        Call.objects.get_or_create(sid=request.GET['CallSid'])

        r = Response()

        r.say('''You have reached the St. Louis homeless help hotline. If you need immediate help, hang up and dial 9 1 1.''')
        with r.gather(finishOnKey='#', method='POST', action=reverse('phone:start'), numDigits=1) as g:
            g.say('If you need a bed tonight, press 1. To speak with a volunteer, press 0.')

        return r

    def post(self, request):
        if request.POST['Digits'] == '1':
            return redirect(reverse('phone:collect_location'))
        elif request.POST['Digits'] == '0':
            return redirect(reverse('phone:operator'))
        else:
            return redirect(reverse('phone:start'))


class CollectLocationView(TwilioView):
    def get(self, request):
        r = Response()
        
        r.say('''"Where are you now? At the tone, please say an address or street intersection in the Saint Louis area. When you are finished, press Pound.''')
        r.record(action=reverse('phone:collect_location'), method='POST', maxLength=10, timeout=2, transcribe=True)

        return r

    def post(self, request):
        # TODO: fill out this stub appropriate GIS conversion
        return redirect(reverse('phone:bed_count'))


class OperatorView(TwilioView):
    def get(self, request):
        r = Request()
        r.say('You will be connected to an operator in the final product. For now, the call is over. Thank you.')
        return r


class BedCountView(TwilioView):
    def get(self, request):
        r = Response()
        r.say('How many beds do you need tonight?')
        with r.gather(finishOnKey='#', method='POST', action=reverse('phone:bed_count'), numdigits=1) as g:
            g.say('Press a number, then press pound')

        return r

    def post(self, request):
        digit = request.POST['Digits']
        if digit in '123456789':
            call, created = Call.objects.get_or_create(sid=request.POST['CallSid'])
            call.bed_count = int(digit)
            call.save()
            
            return redirect(reverse('phone:find_shelter'))
        else:
            return redirect(reverse('phone:bed_count'))


class FindShelterView(TwilioView):
    # TODO: implement this API
    # def setup_call(self, request):
    #     call = Call.objects.get_or_create(sid=request.POST['CallSid'])
    #     shelters = shelter.objects.find_beds_for_location(
    #         bed_count=call.bed_count,
    #         latitude=38.62824, longitude=-90.19069
    #     )
    #     call.constrain(shelters)

    #     return call

    # def get(self, request):
    #     call = self.setup_call(request)
    #     question, kind = call.get_question()

    #     r = Response()
    #     r.say(question)
    #     with r.gather(finishOnKey='#', method='POST', action=reverse('phone:find_shelter'), numdigits=4) as g:
    #         if kind == 'boolean':
    #             g.say('Press 1 for yes, 0 for no and then press pound.')
    #         elif kind == 'int':
    #             g.say('Press pound when finished.')

    #     return r

    def get(self, request):
        shelters = Shelter.objects.all()
        return redirect(reverse('phone:start_shelter_call', kwargs={
            'pks': ','.join([str(s.pk) for s in shelters]),
            'client_call': Call.objects.get_or_create(sid=request.POST['CallSid'])[0].pk
        }))


class ShelterCallView(TwilioView):
    def get(self, request, client_call, pks):
        pks = pks.split(',')
        try:
            shelter = Shelter.objects.get(pk=pks[0])
        except Shelter.DoesNotExist:
            pks = ','.join(pks[1:])
            if pks:
                return redirect(reverse(
                    'phone:start_shelter_call',
                    kwargs={
                        'pks': pks,
                        'client_call': client_call
                    }
                ))

        client.calls.create(
            to=shelter.phone_number,
            from_=settings.TWILIO_CALLER_ID,
            url=redirect(reverse(
                'phone:verify_shelter_availability',
                kwargs={'client_call': client_call}
            )),
            status_callback=redirect(reverse(
                'phone:post_shelter_call',
                kwargs={
                    'pks': ','.join([str(pk) for pk in pks[1:]]),
                    'client_call': client_call
                }
            ))
        )

        r = Response()
        r.say('We are contacting %s. Please hold.' % shelter.name)
        r.enqueue(
            name='waiting_for_shelter',
            wait_url='http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient'
        )
        return r


class PostShelterCallView(TwilioView):
    def get(request, client_call, pks):
        if pks == '':
            return redirect(reverse('phone:operator'))

        pks = pks.split(',')

        call = Call.objects.get(pk=client_call)
        if call.shelter:
            r = Response()
            r.say('%d beds have been reserved for tonight at %s. Their address is %s. Thank you.' % (
                call.bed_count,
                call.shelter.name,
                call.shelter.address
            ))
            return r

        else:
            return redirect(reverse(
                'phone:start_shelter_call',
                kwargs={
                    'pks': pks,
                    'client_call': client_call
                }
            ))

class VerifyShelterAvailabilityView(TwilioView):
    def get():
        r = Response()
        r.say('Is your refrigerator running?')
        return r
