# 1.mapper的配置
``` java
public interface TbCourseMapper {
       List<TbCourse> getWithIds(@Param("params") Map<String,Object> map);
}
```
# 2.mapper.xml文件中的写法
``` xml
<select id="getWithIds" resultType="com.certificate.course_center.po.TbCourse"
            parameterType="Map">
        SELECT *
        FROM tb_course tc
        WHERE course_id in
        <foreach collection="params.ids" item="id" open="(" close=")" separator=",">
            #{id}
        </foreach>
    </select>
```
# 3.service中的写法
``` java
  public List<TbCourse> getCourseWithCourseIds(List<Integer> courseIds) {
        Map<String,Object> map=new HashMap<>();
        map.put("ids",courseIds);
        return tbCourseMapper.getWithIds(map);
    }
```
至此在sql中遍历的列表的功能就完成了
