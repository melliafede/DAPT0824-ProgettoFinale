import chardet

# Read a portion of the file to guess the encoding
with open('tennis_atp-master/atp_matches_1968.csv', 'rb') as f:
    raw_data = f.read(10000)  # Read first 10KB
    result = chardet.detect(raw_data)

print(f"Detected encoding: {result['encoding']} with confidence {result['confidence']:.2f}")
