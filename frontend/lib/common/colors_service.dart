import 'package:flutter/material.dart';

// Note: Must also update custom_theme.dart to match
Map<String, List<double>> _colorMap = {
  'primary': [0, 181, 181],
  'primaryLight': [0, 210, 210],
  'primaryDark': [0, 93, 93],
  'primaryTransparent': [0, 181, 181, 0.4],
  'accent': [0, 164, 203],
  'accentDark': [0, 100, 120, 0.5],
  'accentTransparent': [0, 164, 203, 0.4],
  // 'secondary': [1, 142, 211],
  'secondary': [143, 229, 142],
  'text': [90, 90, 90],
  'error': [169, 46, 97],
  'warning': [220, 145, 110],
  'transparent': [0,0,0,0],

  // 'magentaTransparent': [200, 100, 240, 0.4],
  // 'magenta': [200, 100, 240],
  // 'red': [200, 100, 0],

  'greyLight': [200, 200, 200],
  'grey': [125, 125, 125],
  'greyTransparent': [125, 125, 125, 0.4],
  'greyDark': [50, 50, 50],
  'white': [255, 255, 255],
};
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

  Map<String, Color> _colors = {};
  Map<String, String> _colorsStr = {};

  bool _inited = false;

  void Init() {
    _inited = true;
    for (String key in _colorMap.keys) {
      _colors[key] = valsToColor(_colorMap[key]!);
      _colorsStr[key] = valsToString(_colorMap[key]!);
    }
  }

  Map<String, Color> GetColors() {
    if (!_inited) {
      Init();
    }
    return _colors;
  }

  Map<String, String> GetColorsStr() {
    if (!_inited) {
      Init();
    }
    return _colorsStr;
  }

  // get colors => _colors;
  // get colorsStr => _colorsStr;
  get colors => GetColors();
  get colorsStr => GetColorsStr();
}
