<!-- TOC -->

- [1.引入maven依赖](#1引入maven依赖)
- [2.上传文件](#2上传文件)
- [3.断点上传](#3断点上传)

<!-- /TOC -->
# 1.引入maven依赖
``` xml
  <!--引入阿里oss-->
        <!-- https://mvnrepository.com/artifact/com.aliyun.oss/aliyun-sdk-oss -->
        <dependency>
            <groupId>com.aliyun.oss</groupId>
            <artifactId>aliyun-sdk-oss</artifactId>
            <version>2.2.1</version>
        </dependency>
```
# 2.上传文件
``` java
/**
     * 上传文件到oss,返回上传oss之后的地址
     * @param file
     * @return
     */
    public static String upLoadFIle2Oss(MultipartFile file,String fileDir){
        String ossUrl=null;
            try {
                OSSClientUtil ossClient = new OSSClientUtil();
                String OssImageName = uploadImg2Oss(file,fileDir);
                ossUrl = ossClient.getImgUrl(OssImageName,fileDir);
            }catch (Exception e){
                log.error(e.getMessage());

            }
        


        return ossUrl;
    }
 public String uploadImg2Oss(MultipartFile file,String fileDir){
        String originalFilename = file.getOriginalFilename();
        String substring = originalFilename.substring(originalFilename.lastIndexOf(".")).toLowerCase();
        Random random = new Random();
        String name = random.nextInt(10000) + System.currentTimeMillis() + substring;
        InputStream inputStream = null;
        try {
            inputStream = file.getInputStream();
            this.uploadFile2OSS(inputStream, name,fileDir);
        } catch (IOException e) {
            e.printStackTrace();
        }

        return name;
    }
/**
     * 获得图片路径
     *
     * @param fileUrl
     * @return
     */
    public String getImgUrl(String fileUrl,String fileDir) {
        System.out.println(fileUrl);
        if (!StringUtils.isEmpty(fileUrl)) {
            String[] split = fileUrl.split("/");
            return this.getUrl(fileDir + split[split.length - 1]);
        }
        return null;
    }
      /**
     * 上传到OSS服务器 如果同名文件会覆盖服务器上的
     *
     * @param instream
     *            文件流
     * @param fileName
     *            文件名称 包括后缀名
     * @return 出错返回"" ,唯一MD5数字签名
     */
    public String uploadFile2OSS(InputStream instream, String fileName,String fileDir) {
        String ret = "";
        try {
            // 创建上传Object的Metadata
            ObjectMetadata objectMetadata = new ObjectMetadata();
            objectMetadata.setContentLength(instream.available());
            objectMetadata.setCacheControl("no-cache");
            objectMetadata.setHeader("Pragma", "no-cache");
            objectMetadata.setContentType(getContentType(fileName.substring(fileName.lastIndexOf("."))));
            objectMetadata.setContentDisposition("inline;filename=" + fileName);
            // 上传文件
            PutObjectResult putResult = ossClient.putObject(bucketName, fileDir + fileName, instream, objectMetadata);
            ret = putResult.getETag();
        } catch (IOException e) {
            logger.error(e.getMessage(), e);
        } finally {
            try {
                if (instream != null) {
                    instream.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return ret;
    }
```
# 3.断点上传
``` java
 /**
     * 上传视频文件到oss,返回上传oss之后的地址
     * @param file
     * @return
     */
    public static String upLoadVideo2Oss(MultipartFile file,String dir){
        String ossUrl=null;
            try {
                OSSClientUtil ossClient = new OSSClientUtil();
                File newFile=MultipartFile2File( file);
                String OssImageName = ossClient.uploadVideo2OSS(newFile.getPath(),newFile.getName(),dir);
                ossUrl = ossClient.getUrl(OssImageName);
                if(ossUrl!=null&&!"".equals(ossUrl)){
                    newFile.delete();
                }
            }catch (Exception e){
                log.error(e.getMessage());
            }
        

        return ossUrl;
    }
    public class OSSClientUtil {
public static final Logger logger = LoggerFactory.getLogger(OSSClientUtil.class);
    // endpoint
    // endpoint以杭州为例，其它region请按实际情况填写
    private static final String endpoint = "http://oss-cn-hangzhou.aliyuncs.com";
    // accessKey
    private static final String accessKeyId = "LTAIBV6mlkfxp7l";
    private static final String accessKeySecret = "TyyLM1HzNdujedZ6dmF9A2xshzScjUS";
    // 空间
    private String bucketName = "bqkj";
    //用户
    //头像
    private static String USER_PROFILE_IMAGE = "bqkj/campusGang/userInfo/profileImage/";
    //内容管理
    //附件
    public static String CONTENT_MANAGE_ACCESSORY = "bqkj/campusGang/ContentManagement/Accessory/";
    //富文本内容
    public static String CONTENT_MANAGE_RICH_TEXT = "bqkj/campusGang/ContentManagement/RichTextContent/";
    //缩略图
    public static String CONTENT_MANAGE_THUMBNAIL = "bqkj/campusGang/ContentManagement/Accessory/";
    //留言
    //缩略图
    public static String LEAVE_MSG_IMAGE = "bqkj/campusGang/leaveMsg/image/";
    public static String INVOICE_OCR = "bqkj/campusGang/invoice/ocr/";
    private OSSClient ossClient;

    public OSSClientUtil() {
        ossClient = new OSSClient(endpoint, accessKeyId, accessKeySecret);
    }

    /**
     * 初始化
     */
    public void init() {
        ossClient = new OSSClient(endpoint, accessKeyId, accessKeySecret);
    }

    /**
     * 销毁
     */
    public void destory() {
        ossClient.shutdown();
    }

    /**
     * 上传图片
     *
     * @param url
     */
    public void uploadImg2Oss(String url,String fileDir){
        File fileOnServer = new File(url);
        FileInputStream fin;
        try {
            fin = new FileInputStream(fileOnServer);
            String[] split = url.split("/");
            this.uploadFile2OSS(fin, split[split.length - 1],fileDir);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }


    }

    public String uploadImg2Oss(MultipartFile file,String fileDir){
        String originalFilename = file.getOriginalFilename();
        String substring = originalFilename.substring(originalFilename.lastIndexOf(".")).toLowerCase();
        Random random = new Random();
        String name = random.nextInt(10000) + System.currentTimeMillis() + substring;
        InputStream inputStream = null;
        try {
            inputStream = file.getInputStream();
            this.uploadFile2OSS(inputStream, name,fileDir);
        } catch (IOException e) {
            e.printStackTrace();
        }

        return name;
    }

    /**
     * 获得图片路径
     *
     * @param fileUrl
     * @return
     */
    public String getImgUrl(String fileUrl,String fileDir) {
        System.out.println(fileUrl);
        if (!StringUtils.isEmpty(fileUrl)) {
            String[] split = fileUrl.split("/");
            return this.getUrl(fileDir + split[split.length - 1]);
        }
        return null;
    }

    /**
     * 上传到OSS服务器 如果同名文件会覆盖服务器上的
     *
     * @param instream
     *            文件流
     * @param fileName
     *            文件名称 包括后缀名
     * @return 出错返回"" ,唯一MD5数字签名
     */
    public String uploadFile2OSS(InputStream instream, String fileName,String fileDir) {
        String ret = "";
        try {
            // 创建上传Object的Metadata
            ObjectMetadata objectMetadata = new ObjectMetadata();
            objectMetadata.setContentLength(instream.available());
            objectMetadata.setCacheControl("no-cache");
            objectMetadata.setHeader("Pragma", "no-cache");
            objectMetadata.setContentType(getContentType(fileName.substring(fileName.lastIndexOf("."))));
            objectMetadata.setContentDisposition("inline;filename=" + fileName);
            // 上传文件
            PutObjectResult putResult = ossClient.putObject(bucketName, fileDir + fileName, instream, objectMetadata);
            ret = putResult.getETag();
        } catch (IOException e) {
            logger.error(e.getMessage(), e);
        } finally {
            try {
                if (instream != null) {
                    instream.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return ret;
    }

    /**
     * 断点上传视频
     * @param filePath
     * @param fileName
     * @return
     */
    public String uploadVideo2OSS(String filePath, String fileName,String dir) {
        String ret = "";
        try {
            fileName=dir+new Date().getTime()+fileName;
            UploadFileRequest uploadFileRequest = new UploadFileRequest(bucketName, fileName);
            // The local file to upload---it must exist.
            uploadFileRequest.setUploadFile(filePath);
            // Sets the concurrent upload task number to 5.
            uploadFileRequest.setTaskNum(6);
            // Sets the part size to 1MB.
            uploadFileRequest.setPartSize(1024 * 1024 * 1);
            // Enables the checkpoint file. By default it's off.
            uploadFileRequest.setEnableCheckpoint(true);

            UploadFileResult uploadResult = ossClient.uploadFile(uploadFileRequest);

            CompleteMultipartUploadResult multipartUploadResult =
                    uploadResult.getMultipartUploadResult();
            ret=fileName;
            System.out.println(multipartUploadResult.getETag());
        }  catch (OSSException oe) {
            System.out.println("Caught an OSSException, which means your request made it to OSS, "
                    + "but was rejected with an error response for some reason.");
            System.out.println("Error Message: " + oe.getErrorMessage());
            System.out.println("Error Code:       " + oe.getErrorCode());
            System.out.println("Request ID:      " + oe.getRequestId());
            System.out.println("Host ID:           " + oe.getHostId());
        } catch (ClientException ce) {
            System.out.println("Caught an ClientException, which means the client encountered "
                    + "a serious internal problem while trying to communicate with OSS, "
                    + "such as not being able to access the network.");
            System.out.println("Error Message: " + ce.getMessage());
        } catch (Throwable e) {
            e.printStackTrace();
        } finally {
            ossClient.shutdown();
        }
        return ret;
    }

    /**
     * 删除oss的文件，传参是bqkj/campusGang/userInfo/profileImage/1590730407032.jpg
     * @param filePath
     * @return
     */
    public boolean deleteOssFile(String filePath) {
        boolean exist = ossClient.doesObjectExist(bucketName, filePath);
        if (!exist) {
            logger.error("文件不存在,filePath={}", filePath);
            return false;
        }
        logger.info("删除文件,filePath={}", filePath);
        ossClient.deleteObject(bucketName, filePath);
        ossClient.shutdown();
        return true;
    }

    /**
     * Description: 判断OSS服务文件上传时文件的contentType
     * @param filenameExtension 文件后缀
     * @return String
     */
    public static String getContentType(String filenameExtension) {
        if (filenameExtension.equalsIgnoreCase(".bmp")) {
            return "image/bmp";
        }
        if (filenameExtension.equalsIgnoreCase(".gif")) {
            return "image/gif";
        }
        if (filenameExtension.equalsIgnoreCase(".jpeg") || filenameExtension.equalsIgnoreCase(".jpg")
                || filenameExtension.equalsIgnoreCase(".png")) {
            return "image/jpeg";
        }
        if (filenameExtension.equalsIgnoreCase(".html")) {
            return "text/html";
        }
        if (filenameExtension.equalsIgnoreCase(".txt")) {
            return "text/plain";
        }
        if (filenameExtension.equalsIgnoreCase(".vsd")) {
            return "application/vnd.visio";
        }
        if (filenameExtension.equalsIgnoreCase(".pptx") || filenameExtension.equalsIgnoreCase(".ppt")) {
            return "application/vnd.ms-powerpoint";
        }
        if (filenameExtension.equalsIgnoreCase(".docx") || filenameExtension.equalsIgnoreCase(".doc")) {
            return "application/msword";
        }
        if (filenameExtension.equalsIgnoreCase(".xml")) {
            return "text/xml";
        }
        if (filenameExtension.equalsIgnoreCase(".pdf")) {
            return "application/pdf";
        }
        return "image/jpeg";
    }

    /**
     * 获得url链接
     *
     * @param key
     * @return
     */
    public String getUrl(String key) {
        // 设置URL过期时间为10年 3600l* 1000*24*365*10

        Date expiration = new Date(System.currentTimeMillis() + 3600L * 1000 * 24 * 365 * 10);
        // 生成URL
        URL url = ossClient.generatePresignedUrl(bucketName, key, expiration);
        if (url != null) {
            return url.toString();
        }
        return null;
    }

    }
     
```
