import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# --- 1. AYARLAR ---
years = [2024, 2025, 2026]
global_end_date = datetime(2026, 3, 15)
start_date = datetime(2024, 1, 1)

# --- 2. DÖVİZ KURLARI MASTER ---
currency_history = []
base_rates = {'USD': 30.0, 'EUR': 33.0, 'GBP': 38.0, 'AED': 8.2}
monthly_growth = 1.018

temp_date = start_date
while temp_date <= global_end_date:
    month_key = temp_date.strftime('%Y-%m')
    row = {'Ay_Yil': month_key}
    for curr, rate in base_rates.items():
        months_passed = (temp_date.year - 2024) * 12 + temp_date.month - 1
        row[curr] = round(rate * (monthly_growth ** months_passed), 4)
    currency_history.append(row)
    temp_date = (temp_date.replace(day=1) + timedelta(days=32)).replace(day=1)
df_doviz_kurlari = pd.DataFrame(currency_history)

# --- 3. ŞEHİRLER (Aynen Korundu) ---
city_data = [
    [1, 'İstanbul', 'Marmara'], [2, 'Ankara', 'İç Anadolu'], [3, 'İzmir', 'Ege'],
    [4, 'Bursa', 'Marmara'], [5, 'Antalya', 'Akdeniz'], [6, 'Adana', 'Akdeniz'],
    [7, 'Konya', 'İç Anadolu'], [8, 'Gaziantep', 'Güneydoğu'], [9, 'Kocaeli', 'Marmara'],
    [10, 'Mersin', 'Akdeniz'], [11, 'Diyarbakır', 'Güneydoğu'], [12, 'Samsun', 'Karadeniz'],
    [13, 'Denizli', 'Ege'], [14, 'Eskişehir', 'İç Anadolu'], [15, 'Trabzon', 'Karadeniz'],
    [16, 'Aydın', 'Ege'], [17, 'Tekirdağ', 'Marmara'], [18, 'Kayseri', 'İç Anadolu'],
    [19, 'Londra İngiltere', 'İngiltere'], [20, 'Berlin', 'Almanya'], [21, 'Dubai', 'BAE'], [22, 'New York', 'ABD']
]
df_sehirler = pd.DataFrame(city_data, columns=['SehirID', 'Sehir_Adi', 'Bolge'])

# --- 4. ÜRÜNLER (Aynen Korundu) ---
product_raw = [
    [2001, 'Ethiopia Yirgacheffe 250g', 'Kahve', 250], [2002, 'Colombia Huila 250g', 'Kahve', 250],
    [2003, 'Brazil Santos 500g', 'Kahve', 500], [2004, 'Guatemala Antigua 250g', 'Kahve', 250],
    [2005, 'Sumatra Mandheling 1kg', 'Kahve', 1000], [2006, 'Kenya AA Nyeri 250g', 'Kahve', 250],
    [2007, 'Costa Rica Tarrazu 250g', 'Kahve', 250], [3001, 'House Blend 500g', 'Kahve', 500],
    [3002, 'Espresso Roast 1kg', 'Kahve', 1000], [3003, 'Cold Brew Blend 1kg', 'Kahve', 1000],
    [4001, 'V60 Demleme Seti', 'Donanım', 1500], [4002, 'Elektrikli Öğütücü Pro', 'Cihaz', 3000],
    [4003, 'French Press 600ml', 'Donanım', 800], [4004, 'Moka Pot 3 Cup', 'Donanım', 600],
    [4005, 'Hassas Tartı 0.1g', 'Aksesuar', 300]
]
df_urunler = pd.DataFrame(product_raw, columns=['UrunID', 'Urun_Adi', 'Urun_Tipi', 'Boyut_Gram'])
df_urunler['Boyut_KG'] = df_urunler['Boyut_Gram'] / 1000

# --- 5. SATIŞ SORUMLULARI (Aynen Korundu) ---
reps_data = [
    [101, 'Ahmet Yılmaz', 'Marmara'], [102, 'Canan Kaya', 'Marmara'], [103, 'Mehmet Demir', 'İç Anadolu'],
    [104, 'Ayşe Tekin', 'Ege'], [105, 'Oğuzhan Çelik', 'Akdeniz'], [106, 'Selin Aydın', 'Karadeniz'],
    [107, 'John Smith', 'İngiltere'], [108, 'Elena Müller', 'Almanya'], [109, 'Ahmed Al-Farsi', 'BAE'],
    [110, 'David Brown', 'ABD'], [111, 'Zeynep Bulut', 'Marmara'], [112, 'Murat Yıldız', 'İç Anadolu']
]
df_satis_sorumlulari_master = pd.DataFrame(reps_data, columns=['SorumluID', 'Sorumlu_Adi', 'Sorumlu_Bolgesi'])

# --- 6. SATIŞ NOKTALARI (Aynen Korundu) ---
brand_config = {
    'Starbucks': 'Horeca', 'Kahve Dünyası': 'Horeca', 'Espresso Lab': 'Horeca',
    'Migros': 'Retail', 'CarrefourSA': 'Retail', 'Macrocenter': 'Retail',
    'Amazon': 'Online', 'Getir': 'Online'
}
points = []
brand_list = list(brand_config.keys())
for i in range(1, 61):
    brand = random.choice(brand_list)
    points.append({
        'NoktaID': 8000 + i,
        'Nokta_Adi': f"{brand} - Şube {i}",
        'Zincir_Adi': brand,
        'Kanal': brand_config[brand],
        'SehirID': random.choice(df_sehirler['SehirID'].values)
    })
df_satis_noktalari_master = pd.DataFrame(points)

# --- 7. FİYAT LİSTESİ ---
price_rows = []
for _, row in df_urunler.iterrows():
    base_try = 480 if row['Urun_Tipi'] == 'Kahve' else 2400
    for yr in years:
        # Enflasyonist artış: 2024 baz, 2025 +%55, 2026 +%110
        inf = 1.0 if yr == 2024 else (1.55 if yr == 2025 else 2.1)
        try_price = base_try * inf
        jan_rates = df_doviz_kurlari[df_doviz_kurlari['Ay_Yil'] == f"{yr}-01"].iloc[0]
        
        price_rows.append({
            'Yil': yr, 'UrunID': row['UrunID'],
            'TRY': round(try_price, 2),
            'USD': round(try_price / jan_rates['USD'], 2),
            'EUR': round(try_price / jan_rates['EUR'], 2),
            'GBP': round(try_price / jan_rates['GBP'], 2),
            'AED': round(try_price / jan_rates['AED'], 2)
        })
df_fiyat_listesi = pd.DataFrame(price_rows)

# --- 8. SATIŞ & SATIŞ FİNANSAL (Düzeltilmiş Formüller) ---
sales, finance = [], []
curr, s_id = start_date, 1
bolge_to_curr = {'İngiltere': 'GBP', 'Almanya': 'EUR', 'BAE': 'AED', 'ABD': 'USD'}

while curr <= global_end_date:
    month_key = curr.strftime('%Y-%m')
    # Satış ve Kar Azalmasını Engellemek İçin Büyüme Faktörü (Yıllık %30 artış trendi)
    growth_factor = 1.0 + ((curr.year - 2024) * 0.3) + (curr.month * 0.01)
    
    for _ in range(random.randint(5, 15)):
        pt = df_satis_noktalari_master.sample(1).iloc[0]
        prod = df_urunler.sample(1).iloc[0]
        sehir_info = df_sehirler[df_sehirler['SehirID'] == pt['SehirID']].iloc[0]
        bolge = sehir_info['Bolge']
        
        # Sorumlu Atama
        bolge_reps = df_satis_sorumlulari_master[df_satis_sorumlulari_master['Sorumlu_Bolgesi'] == bolge]
        rep_id = random.choice(bolge_reps['SorumluID'].values) if not bolge_reps.empty else random.choice(df_satis_sorumlulari_master['SorumluID'].values)
            
        currency = bolge_to_curr.get(bolge, 'TRY')
        base_try_price = df_fiyat_listesi[(df_fiyat_listesi['UrunID'] == prod['UrunID']) & (df_fiyat_listesi['Yil'] == curr.year)]['TRY'].values[0]
        
        # --- DÜZELTİLMİŞ FİNANSAL HESAPLAMA BLOĞU ---
        qty = int(random.randint(1, 10) * growth_factor) # Satış trendini korur
        unit_price = base_try_price 
        
        # Temel Satış Değerleri
        net_satis_try = unit_price * qty
        iskonto_try = net_satis_try * random.uniform(0.05, 0.15)
        brut_ciro_try = net_satis_try + iskonto_try 
        
        # Vergiler
        otv_ratio = 0.20 if 'Öğütücü' in prod['Urun_Adi'] else (0.05 if 'Tartı' in prod['Urun_Adi'] else 0.0)
        export_tax_ratio = 0.08 if currency != 'TRY' else 0.00
        
        otv_try = net_satis_try * otv_ratio
        kdv_try = net_satis_try * 0.20 # Net Satış üzerinden %20 KDV
        export_tax_try = net_satis_try * export_tax_ratio
        
        # Operasyonel Maliyetler
        cogs_try = net_satis_try * random.uniform(0.30, 0.35)
        opex_try = net_satis_try * random.uniform(0.10, 0.15)
        
        # EBIT Denklem Sabitleme (İstediğin Tam Karşılama Mantığı)
        # Net Satış = EBIT + COGS + OPEX + OTV + KDV + Export_Tax
        ebit_try = net_satis_try - (cogs_try + opex_try + otv_try + kdv_try + export_tax_try)
        
        sales.append({
            'SatisID': s_id, 'Tarih': curr, 'NoktaID': pt['NoktaID'], 'UrunID': prod['UrunID'], 
            'SorumluID': rep_id, 'Miktar': qty, 'Toplam_KG': round(qty * prod['Boyut_KG'], 2), 'Currency': currency
        })
        finance.append({
            'Satis_ID': s_id, 'Brut_Ciro': round(brut_ciro_try, 2), 'Iskonto': round(iskonto_try, 2),
            'Net_Satis': round(net_satis_try, 2), 'OTV': round(otv_try, 2),
            'KDV': round(kdv_try, 2), 'Export_Tax': round(export_tax_try, 2),
            'COGS': round(cogs_try, 2), 'OPEX': round(opex_try, 2), 'EBIT': round(ebit_try, 2)
        })
        s_id += 1
    curr += timedelta(days=1)

# --- 9. HEDEF GENEL (Düzeltilmiş KG Hesaplaması) ---
df_sales_all = pd.merge(pd.DataFrame(sales), pd.DataFrame(finance), left_on='SatisID', right_on='Satis_ID')
actual_daily = df_sales_all.groupby(['Tarih', 'SorumluID', 'UrunID']).agg({
    'Miktar': 'sum', 'Net_Satis': 'sum', 'EBIT': 'sum', 'COGS': 'sum', 'OPEX': 'sum'
}).reset_index()

targets = []
# --- DÜZELTİLMİŞ HEDEF KG BLOĞU ---
for _, row in actual_daily.iterrows():
    # Ürünün birim ağırlığını Master tablodan çekiyoruz
    prod_weight = df_urunler[df_urunler['UrunID'] == row['UrunID']]['Boyut_KG'].values[0]
    f = random.uniform(1.05, 1.15) # Hedef katsayısı
    
    h_adet = int(row['Miktar'] * f) # Hedeflenen adet
    
    targets.append({
        'Tarih': row['Tarih'], 
        'SorumluID': row['SorumluID'], 
        'UrunID': row['UrunID'], 
        'Hedef_Adet': h_adet,
        'Hedef_KG': round(h_adet * prod_weight, 2), # DÜZELTME: Hedef Adet * Birim Ağırlık
        'Hedef_Net_Satis': round(row['Net_Satis'] * f, 2),
        'Hedef_EBIT': round(row['EBIT'] * f, 2)
    })
df_hedef_genel = pd.DataFrame(targets)

# --- 10. KAYIT ---
df_fiyat_listesi.to_csv('Fiyat_Listesi.csv', index=False)
pd.DataFrame(finance).to_csv('Satis_Finansal.csv', index=False)
pd.DataFrame(sales).to_csv('Satis.csv', index=False)
df_satis_noktalari_master.to_csv('Satis_Noktalari_Master.csv', index=False)
df_satis_sorumlulari_master.to_csv('Satis_Sorumlulari_Master.csv', index=False)
df_sehirler.to_csv('Sehirler.csv', index=False)
df_urunler.to_csv('Urunler.csv', index=False)
df_doviz_kurlari.to_csv('Doviz_Kurlari.csv', index=False)
df_hedef_genel.to_csv('Hedef_Genel.csv', index=False)

print("İşlem Tamam: Finansal dengeler sağlandı, hedef KG hesaplaması düzeltildi ve 2024-2026 büyüme trendi eklendi.")