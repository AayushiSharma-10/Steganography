import wave
import numpy as np

class Audio_Steganography:

    def load_audio(self, file_name):
        audio = wave.open(file_name, 'rb')
        para = audio.getparams()
        n_frame = audio.getnframes()
        audio_data = np.frombuffer(audio.readframes(n_frame), dtype= np.int16)
        audio.close()
        return audio_data, para

    def msg_to_bits(self, msgs):
        msgs += '###'
        return ''.join(f"{ ord(c):08b}" for c in msgs)

    def encode_mesg(self, audio_data, secret_message):
        bits = self.msg_to_bits(secret_message)

        if len(bits) > len(audio_data)//2 :
            raise ValueError("Secret Message is too large to hide in this audio file. ")
        

        encoded_data = np.copy(audio_data)
        for i, bit in enumerate(bits):
            encoded_data[2*i] = audio_data[2*i] | int(bit)

        return encoded_data

    def save_audio(self, encoded_data, param, output_path):
        with wave.open(output_path, 'wb') as audio:
            audio.setparams(param)
            audio.writeframes( encoded_data.tobytes() )
    
    def decode_mesg(self, stego_audio):
        audio_data, param = self.load_audio(stego_audio)
        bits = [ (audio_data[2*i] & 1) for i in range( len(audio_data)//2 )]

        chunks = [bits[i:i + 8] for i in range(0, len(bits), 8)]
        decoded_message = ''.join([ chr(int( ''.join(map(str, byte)), 2)) for byte in chunks])

        secret_msg = decoded_message.split('###')[0]
        return secret_msg

original_audio = 'C:/Users/Aayushi Sharma/Desktop/cyber PBL/Stenganography/input.wav'
stego_audio = 'C:/Users/Aayushi Sharma/Desktop/cyber PBL/Stenganography/stego_output.wav'
secret_message = "Hello, Audio Steganography in done !!! "

audio_obj = Audio_Steganography()
audio_data, param = audio_obj.load_audio(original_audio)
encoded_data = audio_obj.encode_mesg(audio_data, secret_message)

audio_obj.save_audio(encoded_data, param, stego_audio)

decoded_data = audio_obj.decode_mesg(stego_audio)

print("Decoded Message : ", decoded_data)