const Number = {
  padWithZeroes(number, length) {
    var value = '' + number;
    while (value.length < length) {
      value = '0' + value;
    }
    return value;
  },
};

export default Number;
