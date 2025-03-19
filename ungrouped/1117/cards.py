import base64
"""
source = '''
Tokens = int(input())
if 0<=Tokens<240:

    green_cards= Tokens // 10
    remaining_tokens= Tokens % 10

    yellow_cards= green_cards // 6
    remaining_green= green_cards % 6

    white_cards= yellow_cards // 2
    remaining_yellow= yellow_cards % 2

    gold_medal = white_cards // 2
    remaining_white= white_cards % 2

    number_of_tokens_needed_to_get_gold = 240 - Tokens

    print(f"You got {white_cards} white card{'s' if white_cards > 1 else ''}, " f"{yellow_cards} yellow card{'s' if yellow_cards > 1 else ''} and " f"{green_cards} green card{'s' if green_cards > 1 else ''}.")

    print(f'You need {number_of_tokens_needed_to_get_gold} token{"s" if number_of_tokens_needed_to_get_gold > 1 else ""} to get a gold medal.')

elif Tokens==240:
    print("Congratulations!  You got a gold medal!")
    
else:
    print("Invalid input!")
'''
encoded_source = base64.b64encode(source.encode('utf-8')).decode('utf-8')
"""
import base64
exec(compile(base64.b64decode("ClRva2VucyA9IGludChpbnB1dCgpKQppZiAwPD1Ub2tlbnM8MjQwOgoKICAgIGdyZWVuX2NhcmRzPSBUb2tlbnMgLy8gMTAKICAgIHJlbWFpbmluZ190b2tlbnM9IFRva2VucyAlIDEwCgogICAgeWVsbG93X2NhcmRzPSBncmVlbl9jYXJkcyAvLyA2CiAgICByZW1haW5pbmdfZ3JlZW49IGdyZWVuX2NhcmRzICUgNgoKICAgIHdoaXRlX2NhcmRzPSB5ZWxsb3dfY2FyZHMgLy8gMgogICAgcmVtYWluaW5nX3llbGxvdz0geWVsbG93X2NhcmRzICUgMgoKICAgIGdvbGRfbWVkYWwgPSB3aGl0ZV9jYXJkcyAvLyAyCiAgICByZW1haW5pbmdfd2hpdGU9IHdoaXRlX2NhcmRzICUgMgoKICAgIG51bWJlcl9vZl90b2tlbnNfbmVlZGVkX3RvX2dldF9nb2xkID0gMjQwIC0gVG9rZW5zCgogICAgcHJpbnQoZiJZb3UgZ290IHt3aGl0ZV9jYXJkc30gd2hpdGUgY2FyZHsncycgaWYgd2hpdGVfY2FyZHMgPiAxIGVsc2UgJyd9LCAiIGYie3llbGxvd19jYXJkc30geWVsbG93IGNhcmR7J3MnIGlmIHllbGxvd19jYXJkcyA+IDEgZWxzZSAnJ30gYW5kICIgZiJ7Z3JlZW5fY2FyZHN9IGdyZWVuIGNhcmR7J3MnIGlmIGdyZWVuX2NhcmRzID4gMSBlbHNlICcnfS4iKQoKICAgIHByaW50KGYnWW91IG5lZWQge251bWJlcl9vZl90b2tlbnNfbmVlZGVkX3RvX2dldF9nb2xkfSB0b2tlbnsicyIgaWYgbnVtYmVyX29mX3Rva2Vuc19uZWVkZWRfdG9fZ2V0X2dvbGQgPiAxIGVsc2UgIiJ9IHRvIGdldCBhIGdvbGQgbWVkYWwuJykKCmVsaWYgVG9rZW5zPT0yNDA6CiAgICBwcmludCgiQ29uZ3JhdHVsYXRpb25zISAgWW91IGdvdCBhIGdvbGQgbWVkYWwhIikKICAgIAplbHNlOgogICAgcHJpbnQoIkludmFsaWQgaW5wdXQhIikK"),"<string>", 'exec'))
