from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth, Group
from django.conf import settings
from django.contrib import messages
from .models import client, client_membership
import datetime
from datetime import datetime
from datetime import date
import pandas as pd
from io import BytesIO
import xlwt

def member(request):
	my_group = Group.objects.get(name=request.user.username)

	data = client.objects.filter(gym=my_group)
	return render(request, 'member.html', {'data':data})


def add_member(request):
	if request.method == "POST":
		my_group = Group.objects.get(name=request.user.username)

		profile_img = request.FILES.get('profile_img')
		name = request.POST.get('name')
		dob = request.POST.get('dob')
		doa = request.POST.get('doa')
		address = request.POST.get('address')
		phone_number = request.POST.get('phone_number')
		emergency_phone_number = request.POST.get('emergency_phone_number')
		email = request.POST.get('email')
		gender = request.POST.get('gender')
		fname = request.POST.get('fname')
		mname = request.POST.get('mname')
		sname = request.POST.get('sname')

		c = client(profile_image=profile_img, name=name, dob=dob, doa=doa, email=email, address=address, phone_number=phone_number, emergency_phone_number=emergency_phone_number, gender=gender, father_name=fname, mother_name=mname, spouse_name=sname, gym=my_group)
		c.save()

		t = client.objects.get(phone_number=phone_number)
		d = datetime(1960,1,1)
		d1 = datetime.date(d)

		if d1 < t.doa:
			f=1
		else:
			f=0
		return render(request, 'srenew.html', {'t':t, 'f':f})

	else:
		return render(request, 'add_member.html', {})

def subscription(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			c = request.POST.get('client_id')
			time = request.POST.get('time')
			amount = request.POST.get('amount')
			discount = request.POST.get('discount')
			final_amount = request.POST.get('final_amount')
			startdate = request.POST.get('startdate')
			payment_method = request.POST.get('payment_method')
			payment_status = request.POST.get('payment_status')
			date_time_obj = datetime.strptime(startdate, '%Y-%m-%d')
			dtobj = date_time_obj.date()

			if payment_status == "on":
				payment_status = "True"
			else:
				payment_status = "False"


			if time == "Monthly":
				due_date = dtobj + pd.DateOffset(months=1)
			elif time == "Quaterly":
				due_date = dtobj + pd.DateOffset(months=3)
			else:
				due_date = dtobj + pd.DateOffset(months=12)

			t = client.objects.get(id=c)

			t.active = "True"
			t.save()

			m = client_membership(client=t, plan=time, amount=amount, final_amount=final_amount, discount=discount, due_date=due_date, date=startdate, payment_method=payment_method, paid=payment_status)
			m.save()
			return redirect('/Profile/')

		else:
			return redirect('/Member')
	else:
		return redirect('/LogIn')

def profile(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			c = request.POST.get('client_id')
			t = client.objects.get(id=c)
			d = datetime(1960,1,1)
			d1 = datetime.date(d)

			m = client_membership.objects.filter(client=t)
			w = m.order_by('-id')
			lw = m.last()
			d2 = date.today()
			d3 = lw.due_date

			if d2 > d3:
				p=1
			else:
				p=0

			if d1 < t.doa:
				f=1
			else:
				f=0
			return render(request, 'phistory.html', {'t':t, 'f':f, 'w':w, 'p':p})
		else:
			return redirect('/Member/')
	else:
		return redirect('/LogIn/')

def prenew(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			c = request.POST.get('client_id')
			t = client.objects.get(id=c)
			d = datetime(1960,1,1)
			d1 = datetime.date(d)

			if d1 < t.doa:
				f=1
			else:
				f=0
			return render(request, 'srenew.html', {'t':t, 'f':f})
		else:
			return redirect('/Member/')
	else:
		return redirect('/LogIn/')


def psubscription(request, m):
	if request.user.is_authenticated:
		t = client.objects.get(phone_number=m)
		d = datetime(1960,1,1)
		d1 = datetime.date(d)

		if d1 < t.doa:
			f=1
		else:
			f=0
		return render(request, 'srenew.html', {'t':t, 'f':f})
	else:
		return redirect('/LogIn/')

def psearch(request):
	if request.method == "POST":
		c = request.POST.get('search')

		my_group = Group.objects.get(name=request.user.username)
		data = client.objects.filter(gym=my_group)
		
		t = data.filter(name__icontains=c)
		return render(request, 'member.html', {'data':t})
	else:
		return redirect('/Member/')


def exportpdf(request):
	my_group = Group.objects.get(name=request.user.username)
	data = client.objects.filter(gym=my_group)

	h=""
	d = datetime(1960,1,1)
	d1 = datetime.date(d)

	response = HttpResponse(content_type='application/vnd.ms-excel') 
	response['Content-Disposition'] = 'attachment;filename=Members.xls' 

	work_book = xlwt.Workbook(encoding = 'utf-8') 
	work_sheet = work_book.add_sheet(u'Members Info')

	style_head_row = xlwt.easyxf("""    
    align:
      wrap off,
      vert center,
      horiz center;
    borders:
      left THIN,
      right THIN,
      top THIN,
      bottom THIN;
    font:
      name Arial,
      colour_index white,
      bold on,
      height 0xA0;
    pattern:
      pattern solid,
      fore-colour 0x19;
    """
    )

	style_data_row = xlwt.easyxf("""
    align:
      wrap on,
      vert center,
      horiz left;
    font:
      name Arial,
      bold off,
      height 0XA0;
    borders:
      left THIN,
      right THIN,
      top THIN,
      bottom THIN;
    """
  	)

	style_data_row.num_format_str = 'M/D/YY'

	work_sheet.write(0,0, 'ID', style_head_row) 
	work_sheet.write(0,1, 'Name', style_head_row) 
	work_sheet.write(0,2, 'Phone Number', style_head_row) 
	work_sheet.write(0,3, 'Emergency Phone Number', style_head_row) 
	work_sheet.write(0,4, 'Email', style_head_row) 
	work_sheet.write(0,5, 'Address', style_head_row)
	work_sheet.write(0,6, 'Date Of Birth', style_head_row)
	work_sheet.write(0,7, 'Gender', style_head_row)
	work_sheet.write(0,8, 'Date Of Anniversary', style_head_row)
	work_sheet.write(0,9, 'Father_Name', style_head_row)
	work_sheet.write(0,10, 'Mother_Name', style_head_row)
	work_sheet.write(0,11, 'Spouse_Name', style_head_row)

	row = 1
	for o in data:
		if o.doa == d1:
			a="-"
		else:
			a=o.doa

		if o.emergency_phone_number == "0000000000":
			b="-"
		else:
			b=str(o.emergency_phone_number)

		work_sheet.write(row,0, str(o.id), style_data_row)
		work_sheet.write(row,1, o.name, style_data_row)
		work_sheet.write(row,2, str(o.phone_number), style_data_row)
		work_sheet.write(row,3, b, style_data_row)
		work_sheet.write(row,4, o.email, style_data_row)
		work_sheet.write(row,5, o.address, style_data_row)
		work_sheet.write(row,6, o.dob, style_data_row)
		work_sheet.write(row,7, o.gender, style_data_row)
		work_sheet.write(row,8, a, style_data_row)
		work_sheet.write(row,9, o.father_name, style_data_row)
		work_sheet.write(row,10, o.mother_name, style_data_row)
		work_sheet.write(row,11, o.spouse_name, style_data_row)

		row=row + 1

	output = BytesIO()
	work_book.save(output)
	output.seek(0)

	response.write(output.getvalue())		
	return response

def expiredmembership(request):
	my_group = Group.objects.get(name=request.user.username)
	data = client.objects.filter(gym=my_group)

	data1 = data.filter(active="False")
	return render(request, 'member1.html', {'data':data1})