

function transform(publish, context) {
    const unixTime = Math.floor(Date.now() / 1000);
    publish.payload.unixtime = unixTime.toString(10);
    const utcTime = new Date().toISOString();
    publish.payload.isotime = utcTime; //"2011-12-19T15:28:46.493Z"
    return publish;
  }