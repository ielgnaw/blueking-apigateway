interface IGateway {
  id: number;
  name: string;
  description: string;
}

interface ISDK {
  language: string;
  version: string;
  url: string;
  name: string;
  install_command: string;
}

interface IResourceVersion {
  id: number;
  version: string;
}

interface ISDKObject {
  gateway: IGateway;
  sdk: ISDK;
  resource_version: IResourceVersion;
  released_stages: any[];
}

export {
  IGateway,
  ISDK,
  IResourceVersion,
  ISDKObject,
};
