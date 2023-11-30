#include "Triangle.hpp"
#include "rasterizer.hpp"
#include <eigen3/Eigen/Eigen>
#include <iostream>
#include <opencv2/opencv.hpp>

constexpr double MY_PI = 3.1415926;

// 视图变换，将相机位置定义到原点位置
Eigen::Matrix4f get_view_matrix(Eigen::Vector3f eye_pos)
{
    Eigen::Matrix4f view = Eigen::Matrix4f::Identity();

    Eigen::Matrix4f translate;
    translate << 1, 0, 0, -eye_pos[0], 0, 1, 0, -eye_pos[1], 0, 0, 1,
        -eye_pos[2], 0, 0, 0, 1;

    view = translate * view;

    return view;
}

// 模型变换，对模型做绕Z旋转
Eigen::Matrix4f get_model_matrix(float rotation_angle)
{
    Eigen::Matrix4f model = Eigen::Matrix4f::Identity();

    Eigen::Matrix4f translate;
    float r = rotation_angle / 180.0 * M_PI;
    translate << cosf(r), -sinf(r), 0, 0, 
                sinf(r), cosf(r), 0, 0, 
                0, 0, 1, 0, 
                0, 0, 0, 1;
    model = translate * model;

    return model;
}

// 透视投影变换
Eigen::Matrix4f get_projection_matrix(float eye_fov, float aspect_ratio,
                                      float zNear, float zFar)
{
    Eigen::Matrix4f projection = Eigen::Matrix4f::Identity();

    Eigen::Matrix4f perspTranslate;
    Eigen::Matrix4f orthoTranslate_center;
    Eigen::Matrix4f orthoTranslate_scale;

    // 计算宽高
    float t = tanf(eye_fov / 180.0 * MY_PI / 2.0) * abs(zNear);
    float b = -t;
    float r = t * aspect_ratio;
    float l = -r;

    // 透视投影 -> 正交投影
    perspTranslate << zNear, 0, 0, 0, 
                    0, zNear, 0, 0, 0, 
                    0, zNear + zFar, - zNear * zFar, 
                    0, 0, 1, 0;
    // 正交投影移动到中心点
    orthoTranslate_center << 1, 0, 0, - (r + l) / 2.0, 
                            0, 1, 0, - (t + b) / 2.0, 
                            0, 0, 1, - (zNear + zFar) / 2.0, 
                            0, 0, 0, 1;
    // scale到cube
    orthoTranslate_scale << 2.0 / (r - l), 0, 0, 0, 
                            0, 2.0 / (t - b), 0, 0, 0, 
                            0, 1 / (zNear - zFar), 0, 
                            0, 0, 0, 1;

    projection =  orthoTranslate_scale * orthoTranslate_center * perspTranslate * projection;

    std::cout << projection << std::endl;
    return projection;
}

int main(int argc, const char** argv)
{
    float angle = 0;
    bool command_line = false;
    std::string filename = "output.png";

    if (argc >= 3) {
        command_line = true;
        angle = std::stof(argv[2]); // -r by default
        if (argc == 4) {
            filename = std::string(argv[3]);
        }
    }

    rst::rasterizer r(700, 700);

    Eigen::Vector3f eye_pos = {0, 0, 5};

    std::vector<Eigen::Vector3f> pos{{2, 0, -2}, {0, 2, -2}, {-2, 0, -2}};

    std::vector<Eigen::Vector3i> ind{{0, 1, 2}};

    auto pos_id = r.load_positions(pos);
    auto ind_id = r.load_indices(ind);

    int key = 0;
    int frame_count = 0;

    if (command_line) {
        r.clear(rst::Buffers::Color | rst::Buffers::Depth);

        r.set_model(get_model_matrix(angle));
        r.set_view(get_view_matrix(eye_pos));
        r.set_projection(get_projection_matrix(45, 1, 0.1, 50));
        // 根据顶点划线
        r.draw(pos_id, ind_id, rst::Primitive::Triangle);
        cv::Mat image(700, 700, CV_32FC3, r.frame_buffer().data());
        image.convertTo(image, CV_8UC3, 1.0f);

        cv::imwrite(filename, image);

        return 0;
    }

    while (key != 27) {
        r.clear(rst::Buffers::Color | rst::Buffers::Depth);

        r.set_model(get_model_matrix(angle));
        r.set_view(get_view_matrix(eye_pos));
        r.set_projection(get_projection_matrix(45, 1, 0.1, 50));

        r.draw(pos_id, ind_id, rst::Primitive::Triangle);

        cv::Mat image(700, 700, CV_32FC3, r.frame_buffer().data());
        image.convertTo(image, CV_8UC3, 1.0f);
        cv::imshow("image", image);
        key = cv::waitKey(10);

        std::cout << "frame count: " << frame_count++ << '\n';

        if (key == 'a') {
            angle += 10;
        }
        else if (key == 'd') {
            angle -= 10;
        }
    }

    return 0;
}
