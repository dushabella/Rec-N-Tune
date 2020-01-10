from scipy.io import wavfile

sample_rate, data = wavfile.read('input_records/Iza10.wav')
# sample_rate, data = wavfile.read('output_records/record.wav')

print(sample_rate)
print(data)

amount_of_samples = len(data)
length_of_sound = amount_of_samples / sample_rate

print("Sample rate:", sample_rate)
print("Amount of samples:", amount_of_samples)
print("Length of sound:", round(length_of_sound, 2), "seconds")
print("Data type:", data.dtype)