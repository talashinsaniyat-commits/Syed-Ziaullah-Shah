import pandas as pd
from datetime import datetime

# ایک بہتر فنکشن جو ٹرانزیکشن لاگز میں لیٹنسی اسپائکس کو ڈھونڈتا ہے اور رپورٹ محفوظ کرتا ہے
def analyze_latency(log_file_path, threshold, output_file='audit_report.csv'):
    """
    ٹرانزیکشن لاگز میں لیٹنسی اسپائکس کا تجزیہ کریں اور نتائج محفوظ کریں
    
    Parameters:
    -----------
    log_file_path : str
        ان پٹ لاگ فائل کا راستہ (CSV فارمیٹ میں)
    threshold : int/float
        لیٹنسی تھریش ہولڈ (ملی سیکنڈ میں)
    output_file : str
        آؤٹ پٹ رپورٹ فائل کا نام (ڈیفالٹ: 'audit_report.csv')
    
    Returns:
    --------
    spikes : DataFrame
        ڈیٹ اسٹیمپ کے ساتھ دریافت شدہ لیٹنسی اسپائکس
    """
    try:
        # لاگ فائل کو لوڈ کریں
        data = pd.read_csv(log_file_path)
        
        # لیٹنسی (Latency) کا موازنہ تھریش ہولڈ سے کریں
        spikes = data[data['latency_ms'] > threshold].copy()
        
        # اگر کوئی اسپائک دریافت ہو تو
        if len(spikes) > 0:
            # موجودہ ٹائم سٹیمپ شامل کریں
            spikes.insert(0, 'report_generated_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            
            # اگر timestamp کالم پہلے سے موجود نہیں ہے تو شامل کریں
            if 'timestamp' not in spikes.columns:
                spikes.insert(1, 'timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            
            # رپورٹ کو CSV میں محفوظ کریں
            spikes.to_csv(output_file, index=False)
            print(f"✓ {len(spikes)} لیٹنسی اسپائکس دریافت ہوئے")
            print(f"✓ رپورٹ '{output_file}' میں محفوظ کر دی گئی")
        else:
            # اگر کوئی اسپائک نہیں ملا
            print(f"ℹ کوئی لیٹنسی اسپائک {threshold}ms سے اوپر نہیں ملے")
            
            # خالی رپورٹ فائل بنائیں
            empty_report = pd.DataFrame(columns=['report_generated_at', 'timestamp', 'latency_ms'])
            empty_report.to_csv(output_file, index=False)
        
        return spikes if len(spikes) > 0 else pd.DataFrame()
        
    except FileNotFoundError:
        print(f"✗ خرابی: فائل '{log_file_path}' نہیں ملی")
        return pd.DataFrame()
    except Exception as e:
        print(f"✗ خرابی: {str(e)}")
        return pd.DataFrame()


# استعمال کا طریقہ
if __name__ == "__main__":
    # مثال کے طور پر استعمال
    # spikes = analyze_latency('transaction_logs.csv', 100)
    # print(spikes)
    
    # یا مختلف آؤٹ پٹ فائل کے ساتھ
    # spikes = analyze_latency('transaction_logs.csv', 100, 'custom_audit_report.csv')
    pass
