from app.models.review import Review
from app.models.business import Business
from app.models.insight import Insight, Sentiment, Issue

b = Business(name='Spice Garden', business_type='restaurant', focus_areas=['delivery', 'quality'])
r = Review(text='Food was cold', business_id='b1')

print('Business:', b.to_dict())
print('Review:', r.to_dict())
print('Models OK')