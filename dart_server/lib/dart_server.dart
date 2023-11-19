import 'package:encrypt/encrypt.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:pointycastle/asymmetric/api.dart';
import 'package:crypto/crypto.dart';

import 'package:encrypt/encrypt.dart' as enc;

String asymmetricEncrypt(String message, String key) {
  RSAKeyParser keyParser = RSAKeyParser();

  RSAAsymmetricKey publicKeyParser = keyParser.parse(key);

  final publicKey =
      RSAPublicKey(publicKeyParser.modulus!, publicKeyParser.exponent!);

  enc.Encrypter encrypter = enc.Encrypter(
      enc.RSA(publicKey: publicKey, encoding: enc.RSAEncoding.PKCS1));

  enc.Encrypted msg = encrypter.encrypt(message);

  return msg.base64;
}

Encrypter createFernetEncrypter(String username, String deviceID) {
  String key = username + deviceID;

  var byte = sha256.convert(utf8.encode(key)).bytes;

  final b64key = Key.fromBase64(base64Url.encode(byte));

  Fernet fernet = Fernet(b64key);
  enc.Encrypter encrypter = enc.Encrypter(fernet);

  return encrypter;
}

void main(List<String> arguments) async {
  enc.Encrypter encrypter = createFernetEncrypter("KAISAN", "");

  String tode =
      "Z0FBQUFBQmxXbkdGYTBKTDQzNVQ1QjNCemlRRnNnYm9XLWI5OVRPWkF2WDE3YmlrVkM4aFQ5a2UzbnBZTk5HX0IwNUwwWUVNeEhpei1yeTdzRjJWYXNyb29oOTZpekxTLXNGMTJJODJueFlYdkdtYVpBQTNBLUt6YkRNdU5OejBtRXlSYnNnX2tOUGVub3BnSjc2MlMwT0ZYbFJqZjlLRDdhRW5nY3JRRlJxOVRTNHdZRngyQ1FfajlNZUtiNXdHWTd6WHhWZFhUSGw4aC1CVlVyTGdIc2t0YWNsQjhQQ0VCb05NaExRUlFCY0ZPMlM5QXNKVFlWWmZfdXcwbEdJSEJlQkpNTVlzU0s4YmVKeXFBdHhEVjZDeEVaUk1ZZFZQSGdXV0dmUDd5dXZvZURPaFdhcGY1VjhGdVRMM1lodzNIQVNlVGRrbkZHUmZyV1ZoVUhVdm1IOGNEeU1VaGszem5PNi0zYUhWTS1aY0hsRGRKeWZaWHRoTGdKUHdEbmRjUENwaEV6OFozRFR3bm51VXUwc0NqOFJkR3dQRGNoUVFxYmFJdlREMzkyZUJGTTN4U2hDQ0xlQk1PTGhnRFltR2RqNExLTEVfV1N3T0V1XzBLTmZRaVZqeTRrTU9BT3VsUzlvaGhuQi1QMzhkcnlVd25fNl8yOWJvRE9kUHFMa25IaEw2cWJYNkdNbm44OHI3Sjl0MGIxMWlldUtXa3FBOFdsNFNrMTUzYU5fS2FMVzk4SlF3RnJqQXg0NExNMXp4NHM5ZHA0RC1OOVliQjFPUFh2b1lxREE4alN1c3puX1VoOW5TdTk2aFRhUFliVEJSQTJzZzQyM25VMEwxNklDZnl3WHE2Tm84cmZSQWp1aU8wRU4tYVRFcHltQmN2b0lhaE83VXNCSDVHQzdVZWMtSUVta3ZoMl8xZDRKLXNIMGVSZU85U25XU0JoWjA5cjdjUnlENjFsSnZGX0NrNjhkdlBhTmVYUmQ3VE0wY0QybVdQdWhPMmVrNkMxUVd1YXFLaXBZZDYwR0h1UjRMRUd0X3VXbmhOZmZqc0FGUmlEZnhNbkI1YnVjaFg2am8wYTVrMk9qQ3FROHZuSjNBbmRnbjhZZkx2YUtfZldpMHFtSVo0Y1htMUNqckxXLVJpSDNrUXRtSU4tMnlEZTR1aTJHSFpka0tuR3pPS19FRnM5R2tGcm1uUFVGOVpadDQ5SXg5SnJEZjJReFRNNnpVZGsxZlY0eERkdzB2Q2kxWkk0MThQYW1saF92Z1RwdEZXN0NtQ3lIY25TNUM5TzEwRWd1dzZSNlBTNkE1REY3UVBxSnFOOFBCNjNBZ1dtZ2ZxUjJnOW03TTZobmc3RlJTZmY0TEdBaC1EMGRQMjNZcklVUTZfWkdqM2gwT0gzTEFZc0wxRUJHd3c1Rmd0THVnM2tsRWNQZlZWYkVONFVXbmlsV1lZdDFHZDdLZ0hiR3JVTzVmbklaMTVycWNiRnVsLU5TV0dlXzF6SXVkNWk4WlNLT096R1AtVnlBPQ==";

  enc.Encrypted encryptedMsg =
      enc.Encrypted.from64(ascii.decode(base64Decode(tode)));

  var decrypted = encrypter.decrypt(encryptedMsg);
  print(decrypted);
  // String replaced = decrypted.replaceAll(r'\', r'\\');
  // print(replaced);
  var js = jsonDecode(decrypted);
  var body2 = jsonEncode({'message': 'secret message'});
  print(js);

  var encrypted = asymmetricEncrypt(body2, js["key"]);
  print(encrypted);

  // var result = await http.post(Uri.parse('http://127.0.0.1:5000/decrypt'),
  //     body: encrypted, headers: header);

  // print(result.body);
}
