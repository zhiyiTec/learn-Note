<!-- TOC -->

- [1.创建目录](#1创建目录)
- [2.获取文件类型](#2获取文件类型)
- [3.MultipartFile 转 File](#3multipartfile-转-file)
- [4. File转 MultipartFile](#4-file转-multipartfile)
- [5.获取MultipartFile文件类型的大小](#5获取multipartfile文件类型的大小)
- [6.压缩图片](#6压缩图片)

<!-- /TOC -->
# 1.创建目录
``` java
/**
     * 判断该路径下的目录是否存在，不存在就生成此目录
     * @param filePath
     * @return
     */
    public static Boolean createDirectory(String filePath){
        Boolean result=true;
        try {
            File file=new File(filePath);
            if (!file.exists()) {
                file.mkdirs();
            }
        }catch (Exception e){
            result=false;
            e.printStackTrace();
        }

        return result;
    }
```
# 2.获取文件类型
``` java
/**
     * 获取文件类型
     * @param file
     * @return
     */
    public static String getFileType(MultipartFile file){
        String fileType=null;
        try {
            String orginName=file.getOriginalFilename();
            String []temp=orginName.split("\\.");
            if(temp.length>1){
                fileType= temp[temp.length-1];
            }
        }catch (Exception e){
            log.error(e.getMessage());

        }
        return fileType;
    }
```
# 3.MultipartFile 转 File
``` java
 /**
     * MultipartFile 转 File
     * @param file
     * @return
     */
    public static File MultipartFile2File(MultipartFile file){
        File re=null;
        try {
            String fileName=new Date().getTime()+file.getOriginalFilename();
            String filePath=PropertyUtil.getProp("pathConfig.properties", "video.local.path");
            File newFile = new File(filePath+fileName);
            file.transferTo(newFile);
            re=newFile;
        }catch (Exception e){
            e.printStackTrace();
        }
        return re;
    }
```
# 4. File转 MultipartFile
``` java

 /**
     * file 转 MultipartFile
     * @param file
     * @return
     */
    public static File MultipartFile2File(File file){
        MultipartFile multipartFile=null;
        try {
            FileInputStream fileInputStream = new FileInputStream(file);
           multipartFile = new MockMultipartFile(file.getName(), file.getName(), ContentType.APPLICATION_OCTET_STREAM.toString(), fileInputStream);
        }catch (Exception e){
            e.printStackTrace();
        }
        return multipartFile;
    }
```
# 5.获取MultipartFile文件类型的大小
``` java
/**
     * 获取MultipartFile文件类型的大小
     * @param file 文件
     * @param sizeTpe 可选择的文件大小类型：B K M G
     * @return
     */
    public static Double getMultipartFileSize(MultipartFile file,String sizeTpe){
        Double fileSize=0.;
        switch (sizeTpe.toUpperCase()){
            case "B":
                fileSize = (double) file.getSize();
                break;
            case "K":
                fileSize = (double) file.getSize()/1024;
                break;
            case "M":
                fileSize = (double) file.getSize()/ 1048576;
                break;
            case "G":
                fileSize = (double) file.getSize()/ 1073741824;
                break;
        }
        return fileSize;
    }
```
# 6.压缩图片
``` java
   /**
     * 压缩图片
     * @param file
     * @return
     */
    public static File compressImage(MultipartFile file){
        File re=null;
        try {
            InputStream inputStream = file.getInputStream();
            // 把图片读入到内存中
            BufferedImage bufImg = ImageIO.read(inputStream);
            // 压缩代码
            // 存储图片文件byte数组
            ByteArrayOutputStream bos = new ByteArrayOutputStream();
            System.out.println(bufImg.getWidth());
            System.out.println(bufImg.getHeight());
            BufferedImage newBufferedImage = new BufferedImage(bufImg.getWidth()-100, bufImg.getHeight()-100,BufferedImage.TYPE_INT_RGB);
            newBufferedImage.createGraphics().drawImage(bufImg, 0, 0, Color.WHITE, null);
            //先转成jpg格式来压缩,然后在通过OSS来修改成源文件本来的后缀格式
            ImageIO.write(newBufferedImage,"jpg",bos);
            //获取输出流
            inputStream = new ByteArrayInputStream(bos.toByteArray());
            String filePath=PropertyUtil.getProp("pathConfig.properties", "video.local.path");
            File newFile=new File(filePath+"\\"+new Date().getTime()+".jpg");
            java.nio.file.Files.copy(
                    inputStream,
                    newFile.toPath(),
                    StandardCopyOption.REPLACE_EXISTING);
            re=newFile;
        }catch (Exception e){
            e.printStackTrace();
        }

        return re;
    }
```
