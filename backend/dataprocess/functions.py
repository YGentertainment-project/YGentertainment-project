import datetime
import openpyxl
from openpyxl.styles import PatternFill, Border, Side, fonts
from openpyxl.styles.alignment import Alignment
from openpyxl.worksheet.cell_range import CellRange
from crawler.serializers import *

from crawler.models import *

DataModels = {
            "youtube": SocialbladeYoutube,
            "tiktok": SocialbladeTiktok,
            "twitter": SocialbladeTwitter,
            "twitter2": SocialbladeTwitter2,
            "weverse": Weverse,
            "instagram": CrowdtangleInstagram,
            "facebook": CrowdtangleFacebook,
            "vlive": Vlive,
            "melon": Melon,
            "spotify": Spotify,
        }

DataSerializers = {
            "youtube": SocialbladeYoutubeSerializer,
            "tiktok": SocialbladeTiktokSerializer,
            "twitter": SocialbladeTwitterSerializer,
            "twitter2": SocialbladeTwitter2Serializer,
            "weverse": WeverseSerializer,
            "instagram": CrowdtangleInstagramSerializer,
            "facebook": CrowdtangleFacebookSerializer,
            "vlive": VliveSerializer,
            "melon": MelonSerializer,
            "spotify": SpotifySerializer,
        }

def convert_to_cell_range(start_row, start_column, end_row, end_column):
    cr = CellRange(range_string=None, min_col=start_column, min_row=start_row,  
                      max_col=end_column, max_row=end_row)
    return cr.coord

def set_border(ws, cell_range, start_row, start_col, style='medium'):
    border_style = Border(left=Side(style=style), 
                     right=Side(style=style), 
                     top=Side(style=style), 
                     bottom=Side(style=style))
    rows = ws[cell_range]
    # one cell
    if len(cell_range) < 5:
        ws.cell(row=start_row, column=start_col).border = border_style
        return
    for row in rows:
        row[0].border = Border(left=Side(style=style))
        row[-1].border = Border(right=Side(style=style))
    for c in rows[0]:
        c.border = Border(top=Side(style=style))
    for c in rows[-1]:
        c.border = Border(bottom=Side(style=style))


def get_platform_data(artist, platform):
    model_fields = DataModels[platform]._meta.fields
    model_fields_name = []
    for model_field in model_fields:
        model_fields_name.append(model_field.name)
    
    #오늘 날짜 기준으로 가져오기
    today_date = datetime.datetime.today()
    filter_objects = DataModels[platform].objects.filter(
        artist = artist,
        recorded_date__year=today_date.year,
        recorded_date__month=today_date.month, recorded_date__day=today_date.day)
    if filter_objects.exists():
        filter_value=filter_objects.values().first()
        #숫자필드값만 보내주기
        filter_datas=[]
        for field_name in model_fields_name:
            if field_name != "id" and field_name != "artist" and field_name != "user_created" and field_name != "recorded_date" and field_name != "platform" and field_name != "url" :
                filter_datas.append(filter_value[field_name])
        return filter_datas
    else:
        filter_datas=[]
        for field_name in model_fields_name:
            if field_name != "id" and field_name != "artist" and field_name != "user_created" and field_name != "recorded_date" and field_name != "platform" and field_name != "url" :
                filter_datas.append("NULL")
        return filter_datas

def export_datareport():
    # 모든 아티스트들
    dummy_artists = [#from facebook.json
        {"artist": "G I-DLE 여자아이들", "follower_num": "745,238"},
        {"artist": "뉴이스트 Nu'est", "follower_num": "2,366,033"},
        {"artist": "레드벨벳 (Red Velvet)", "follower_num": "3,582,560"},
        {"artist": "마마무 Mamamoo", "follower_num": "2,883,145"},
        {"artist": "MONSTA X (몬스타엑스)", "follower_num": "2,832,284"},
        {"artist": "BTS (방탄소년단)", "follower_num": "19,434,509"},
        {"artist": "BLACKPINK", "follower_num": "17,827,522"},
        {"artist": "BIGBANG", "follower_num": "11,662,516"},
        {"artist": "G-DRAGON", "follower_num": "8,914,627"},
        {"artist": "샤이니(SHINee)", "follower_num": "5,706,536"},
        {"artist": "SEVENTEEN", "follower_num": "4,269,422"},
        {"artist": "슈퍼주니어(Super Junior)", "follower_num": "8,448,505"},
        {"artist": "Stray Kids", "follower_num": "2,674,764"},
        {"artist": "ASTRO 아스트로", "follower_num": "2,659,268"},
        {"artist": "aespa", "follower_num": "1,550,987"},
        {"artist": "WINNER", "follower_num": "2,925,657"},
        {"artist": "Cravity - 크래비티", "follower_num": "356,192"},
        {"artist": "TWICE", "follower_num": "7,028,473"},
        {"artist": "AB6IX", "follower_num": "420,116"},
        {"artist": "ATEEZ", "follower_num": "1,138,724"},
        {"artist": "Enhypen", "follower_num": "1,378,647"},
        {"artist": "EXO", "follower_num": "12,409,323"},
        {"artist": "iKON", "follower_num": "3,591,603"},
        {"artist": "ITZY", "follower_num": "2,264,251"},
        {"artist": "NCT", "follower_num": "3,543,987"},
        {"artist": "NCT 127", "follower_num": "3,090,418"},
        {"artist": "NCT DREAM", "follower_num": "1,789,629"},
        {"artist": "더보이즈(THE BOYZ)", "follower_num": "831,445"},
        {"artist": "Treasure 트레저", "follower_num": "1,841,739"},
        {"artist": "TXT (TOMORROW X TOGETHER)", "follower_num": "3,809,914"},
        {"artist": "WayV", "follower_num": "1,153,750"},
        {"artist": "청하 (CHUNG HA)", "follower_num": "966,610"},
        {"artist": "선미 SUNMI", "follower_num": "1,815,662"},
        {"artist": "JEON SOMI (전소미)", "follower_num": "3,727,103"},
        {"artist": "AKMU", "follower_num": "1,034,910"},
        {"artist": "아이유(IU)", "follower_num": "9,550,813"},
        {"artist": "Heize", "follower_num": "460,788"},
        {"artist": "소녀시대(Girls' Generation)", "follower_num": "7,541,708"},
        {"artist": "LEE HI (이하이)", "follower_num": "3,190,599"},
        {"artist": "SECHSKIES", "follower_num": "109,685"},
        {"artist": "볼빨간사춘기", "follower_num": "257,231"},
        {"artist": "HyunA 현아", "follower_num": "3,536,325"},
        {"artist": "BTOB 비투비", "follower_num": "1,735,204"},
        {"artist": "SF9", "follower_num": "972,925"},
        {"artist": "STAYC", "follower_num": "157,485"},
        {"artist": "오마이걸 OH MY GIRL", "follower_num": "675,919"},
        {"artist": "Weeekly - 위클리", "follower_num": "78,426"}
    ]

    # dummy로 값 넣어놓기
    # 서버에서 가져오는 걸로 바꾸자
    dummy_platform_datas = [
        {
            "platform" : "youtube",
            "collect_item": ["uploads","subscribers","views"],
        },
        {
            "platform" : "vlive",
            "collect_item": ["members","videos","likes","plays"],
        },
        # melon이랑 spotify 넣어두기
        {
            "platform" : "instagram",
            "collect_item": ["followers"],
        },
        {
            "platform" : "facebook",
            "collect_item": ["followers"],
        },
        {
            "platform" : "twitter",
            "collect_item": ["followers", "twits"],
        },
        {
            "platform" : "twitter2",
            "collect_item": ["followers", "twits"],
        },
        {
            "platform" : "tiktok",
            "collect_item": ["followers", "uploads","likes"],
        },
        {
            "platform" : "weverse",
            "collect_item": ["weverses"],
        },
    ]
    book = openpyxl.Workbook()
    sheet = book.active
    # sheet.merge_cells() # 어디부터 어디까지 셀 병합

    row = 1
    col = 1

    thin_border = Border(left=Side(style='thin'), 
                     right=Side(style='thin'), 
                     top=Side(style='thin'), 
                     bottom=Side(style='thin'))

    thick_border = Border(left=Side(style='medium'), 
                     right=Side(style='medium'), 
                     top=Side(style='medium'), 
                     bottom=Side(style='medium'))



    sheet.cell(row=1, column=1).value = "플랫폼"
    sheet.cell(row=1, column=1).border = thick_border
    sheet.cell(row=1, column=1).alignment = Alignment(horizontal='center', vertical='center')
    sheet.cell(row=1, column=1).font = fonts.Font(bold=True)

    sheet.cell(row=2, column=1).value = "아티스트"
    sheet.cell(row=2, column=1).border = thick_border
    sheet.cell(row=2, column=1).alignment = Alignment(horizontal='center', vertical='center')
    col += 1
    sheet.row_dimensions[2].height = 35
    sheet.column_dimensions['A'].width = 50

    #플랫폼 이름과 수집항목 띄우기
    for data in dummy_platform_datas:
        sheet.cell(row=row, column=col).value = data["platform"]
        sheet.merge_cells(start_row=row, start_column=col,
            end_row=row, end_column=col+len(data["collect_item"])-1)
        sheet.cell(row=row, column=col).border = thick_border
        sheet.cell(row=row, column=col).alignment = Alignment(horizontal='center', vertical='center')
        sheet.cell(row=row, column=col).font = fonts.Font(bold=True)

        for i, collect_data in enumerate(data["collect_item"]):
            sheet.cell(row=row+1, column=col+i).value = collect_data
            sheet.cell(row=row+1, column=col+i).border = thick_border
            sheet.cell(row=row+1, column=col+i).alignment = Alignment(horizontal='center', vertical='center')
        col += len(data["collect_item"])

    #아티스트별로 플랫폼순서대로 가져와서 띄우기
    row = 3
    col = 1
    for artist in dummy_artists:
        artist_name = artist["artist"]
        sheet.cell(row=row, column=col).value = artist_name
        sheet.cell(row=row, column=col).border = Border(right=Side(style="medium"))
        col += 1
        for platform in dummy_platform_datas:
            #아티스트의 플랫폼마다의 정보 가져오기
            platform_name = platform["platform"]
            platform_data_list = get_platform_data(artist=artist_name, platform=platform_name)
            for i, platform_data in enumerate(platform_data_list):
                if platform_data == "NULL":
                    # null이면 shade 처리
                    sheet.cell(row=row, column=col+i).fill = PatternFill(start_color='C4C4C4', end_color='C4C4C4', fill_type="solid")
                else:
                    sheet.cell(row=row, column=col+i).value = platform_data
            sheet.cell(row=row, column=col+len(platform["collect_item"])-1).border = Border(right=Side(style="medium"))
            col += len(platform["collect_item"])
        row += 1
        col = 1
    return book


def import_datareport(worksheet):
    platform_data_list=[]
    row_num = 0
    for row in worksheet.iter_rows():
        # 플랫폼 정보 나열
        if row_num == 0:
            item_num=0
            platform_name="platform"
            data_json = {}
            for cell in row:
                platform_value = str(cell.value)
                if platform_value == '플랫폼':
                    platform_name = '플랫폼'
                elif platform_value != 'None':
                    if platform_name != '플랫폼':
                        #새로운 게 등장한 거므로 저장
                        data_json["platform"] = platform_name
                        data_json["item_num"] = item_num
                        data_json["item_list"] = []
                        platform_data_list.append(data_json)
                        data_json = {}
                    item_num = 1
                    platform_name = platform_value
                else: #None일때
                    item_num += 1
            #마지막 저장
            data_json["platform"] = platform_name
            data_json["item_num"] = item_num
            data_json["item_list"] = []
            platform_data_list.append(data_json)
            row_num += 1
        # 아티스트 정보 나열
        elif row_num == 1:
            platform_index = 0
            current_index = 0
            for cell in row:
                collect_value = str(cell.value)
                if collect_value != '아티스트':
                    platform_data_list[platform_index]["item_list"].append(collect_value)
                    current_index += 1
                    if current_index >= platform_data_list[platform_index]["item_num"]:
                        platform_index += 1
                        current_index = 0
            print("platform_data_list")
            print(platform_data_list)
            row_num += 1
        # 데이터 정보 나열
        else:
            platform_index = 0
            current_index = 0
            artist_name = "artist"
            data_json = {}
            for i, cell in enumerate(row):
                # 아티스트 이름 나열
                if i==0:
                    artist_name = str(cell.value)
                else:
                    # 아티스트와 플랫폼 이름에 대해 업데이트
                    platform_name = platform_data_list[platform_index]["platform"]
                    collect_value = platform_data_list[platform_index]["item_list"][current_index]
                    value = str(cell.value)
                    if value != 'None':
                        value = int(cell.value)
                        data_json[collect_value] = value
                    current_index += 1
                    if current_index >= platform_data_list[platform_index]["item_num"]:
                        # 데이터 저장
                        data_json["artist"] = artist_name
                        save_collect_data_target(data_json, platform_name)
                        platform_index += 1
                        current_index = 0
                        data_json = {}

def save_collect_data_target(data_json, platform):
    today_date = datetime.datetime.today()
    obj = DataModels[platform].objects.filter(artist=data_json["artist"],recorded_date__year=today_date.year,
                recorded_date__month=today_date.month, recorded_date__day=today_date.day).first()
    if obj is None:
    # 원래 없는 건 새로 저장
        platform_serializer = DataSerializers[platform](data=data_json)
        if platform_serializer.is_valid():
            platform_serializer.save()
    # 있는 건 업데이트
    else:
        platform_serializer = DataSerializers[platform](obj, data=data_json)
        if platform_serializer.is_valid():
            platform_serializer.save()
    # artist 이외 값이 없으면 저장 안됨
