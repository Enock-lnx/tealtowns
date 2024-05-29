class EventClass {
  String id = '', weeklyEventId = '', start = '', end = '', neighborhoodUName = '';

  EventClass(this.id, this.weeklyEventId, this.start, this.end, this.neighborhoodUName);

  EventClass.fromJson(Map<String, dynamic> json) {
    this.id = json.containsKey('_id') ? json['_id'] : json.containsKey('id') ? json['id'] : '';
    this.weeklyEventId = json['weeklyEventId'] ?? '';
    this.start = json['start'] ?? '';
    this.end = json['end'] ?? '';
    this.neighborhoodUName = json['neighborhoodUName'] ?? '';
  }

  Map<String, dynamic> toJson() =>
    {
      '_id': id,
      'weeklyEventId': weeklyEventId,
      'start': start,
      'end': end,
      'neighborhoodUName': neighborhoodUName,
    };
}
