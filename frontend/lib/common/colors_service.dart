import 'package:flutter/material.dart';

List<double> primary = [0, 167, 0];
List<double> secondary = [15, 69, 194];
List<double> primaryLight = [0, 167, 0, 0.5];
List<double> text = [90, 90, 90];

List<double> magentaTransparent = [200, 100, 240, 0.4];
List<double> magenta = magentaTransparent.sublist(0, magentaTransparent.length - 1);
List<double> red = [200, 100, 0];
List<double> greyLight = [200, 200, 200];
List<double> grey = [125, 125, 125];
List<double> greyTransparent = [125, 125, 125, 0.4];
List<double> greyDark = [50, 50, 50];
List<double> white = [255, 255, 255];

String valsToString(List<double> vals) {
  String str = 'rgba(';
  if (vals.length == 3) {
    vals.add(1);
  }
  
  for (int i=0; i<3; i++) {
    str = str + vals[i].toString() + ', ';
  }
  str = str + vals[3].toString() + ')';
  return str;
}

Color valsToColor(List<double> vals) {
  // Assume full opacity if none is provided
  if (vals.length == 3) {
    vals.add(1);
  }
  return Color.fromRGBO(vals[0].toInt(), vals[1].toInt(), vals[2].toInt(), vals[3]);
}
  
class ColorsService {
  ColorsService._privateConstructor();
  static final ColorsService _instance = ColorsService._privateConstructor();
  factory ColorsService() {
    return _instance;
  }

  Map<String, Color> _colors = {
    'primary': valsToColor(primary),
    'secondary': valsToColor(secondary),
    'primaryLight': valsToColor(primaryLight),
    'text': valsToColor(text),

    'greyLight': valsToColor(greyLight),
    'grey': valsToColor(grey),
    'greyTransparent': valsToColor(greyTransparent),
    'greyDark': valsToColor(greyDark),
    'white': valsToColor(white),
    'red': valsToColor(red),
    'magentaTransparent': valsToColor(magentaTransparent),
    'magenta': valsToColor(magenta),
  };

  Map<String, String> _colorsStr = {
    'primary': valsToString(primary),
    'secondary': valsToString(secondary),
    'primaryLight': valsToString(primaryLight),
    'text': valsToString(text),

    'greyLight': valsToString(greyLight),
    'grey': valsToString(grey),
    'greyTransparent': valsToString(greyTransparent),
    'greyDark': valsToString(greyDark),
    'white': valsToString(white),
    'red':  valsToString(red),
    'magentaTransparent': valsToString(magentaTransparent),
    'magenta': valsToString(magenta),
  };

  get colors => _colors;
  get colorsStr => _colorsStr;
}
