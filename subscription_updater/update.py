from members.models import client, client_membership
import datetime
from datetime import datetime
from datetime import date


def sub():
	c = client.objects.all()
	for x in c:
		m = client_membership.objects.filter(client=x)
		lw = m.last()

		d2 = date.today()
		d3 = lw.due_date

		if d2 > d3:
			x.active = "False"
			x.save()