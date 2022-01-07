import datetime
import openpyxl
from openpyxl.styles import PatternFill, Border, Side, fonts
from openpyxl.styles.alignment import Alignment
from config.models import PlatformTargetItem
from dataprocess.models import Platform, Artist
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
    # DB에서 platform과 platform_target_item 가져오기
    db_platform_datas=[]
    platforms = Platform.objects.all()
    if platforms.exists():
        platform_objects_values = platforms.values()
        for platform_value in platform_objects_values:
            collect_item = []
            platform_target_items = PlatformTargetItem.objects.filter(platform_id = platform_value['id'])
            platform_target_items = platform_target_items.values()
            for platform_target_item in platform_target_items:
                collect_item.append(platform_target_item['target_name'])
            db_platform_datas.append({
                "platform" : platform_value['name'],
                "collect_item": collect_item
            })

    # DB에서 artist 가져오기
    db_artists = []
    artists = Artist.objects.all()
    if artists.exists():
        artist_objects_values = artists.values()
        for artist_value in artist_objects_values:
            db_artists.append(artist_value['name'])

    # export excel
    book = openpyxl.Workbook()
    sheet = book.active

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
    for data in db_platform_datas:
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
    for artist in db_artists:
        artist_name = artist
        sheet.cell(row=row, column=col).value = artist_name
        sheet.cell(row=row, column=col).border = Border(right=Side(style="medium"))
        col += 1
        for platform in db_platform_datas:
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
