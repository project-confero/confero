const getTitle = (name: string) =>
  `http://en.wikipedia.org/w/api.php?action=opensearch&search=${encodeURIComponent(
    name
  )}&limit=1&namespace=0&format=json`;

const getExtract = (title: string) =>
  `http://en.wikipedia.org/api/rest_v1/page/summary/${title}`;

const get = async (url: string): Promise<any> => {
  try {
    console.log("getting");
    const response = await fetch(url);
    console.log(response);
    if (!response.ok) throw new Error("error");
    return response.json();
  } catch (e) {
    console.error(e);
    return "";
  }
};

export const fetchInfo = async (name: string) => {
  try {
    const titleResponse = await get(getTitle(name));
    console.log(titleResponse);
    const title = titleResponse[1][0];

    const extractResponse = await get(getExtract(title));
    return extractResponse.extract;
  } catch (e) {
    return "";
  }
};
