export const getPack = (packet: string) => {
  packet = packet.toUpperCase();
  if (packet.includes('X')) {
    let pack = 1;
    // try {
    //     pack = parseInt(packet.substring(0, packet.indexOf('X')));
    // } catch (e) {
    //     return { error: true, message: e.message }
    // }
    try {
      pack = parseInt(packet.substring(packet.indexOf('X') + 1, packet.length));
    } catch (e) {
      return { error: true, message: e.message };
    }
    return { error: false, pack_quantity: pack, pack_description: '' };
  }
  if (packet.includes('T')) {
    packet = packet.replace('T', '');
    packet = packet.replace(' ', '');
    return { error: false, pack_quantity: parseInt(packet), pack_description: packet + 'TAB' };
  }
  if (packet.includes('TAB')) {
    packet = packet.replace('TAB', '');
    packet = packet.replace(' ', '');
    return { error: false, pack_quantity: parseInt(packet), pack_description: packet + 'TAB' };
  }
  if (packet.includes('C')) {
    packet = packet.replace('C', '');
    packet = packet.replace(' ', '');
    return { error: false, pack_quantity: parseInt(packet), pack_description: packet + 'CAP' };
  }
  if (packet.includes('CAP')) {
    packet = packet.replace('CAP', '');
    packet = packet.replace(' ', '');
    return { error: false, pack_quantity: parseInt(packet), pack_description: packet + 'CAP' };
  }
  if (/^\d+$/.test(packet)) {
    return { error: false, pack_quantity: parseInt(packet), pack_description: '' };
  } else {
    return { error: false, pack_quantity: 1, pack_description: packet };
  }
};
