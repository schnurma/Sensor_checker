# Integration of the ${SENSOR_VAR} Sensor from Adafruit and Blinka with the Base Docker Container to run applications which use mraa library
# to run this container use this command for integrated needed folder and privileges
# docker run -it --name <container name> --privileged -v /dev:/dev --network host --group-add dialout  <image name>

FROM ros:galactic-ros-base-focal

USER root

# Variable for the sensor name
# ${variable_name}
# ENV SENSOR_NODE = NODE_PLACE_HOLDER, {Value} will be replaced
# ${SENSOR_NODE} = NODE_PLACEHOLDER
# ENV SENSOR_VAR = SENSOR_PLACE_HOLDER, {Value} will be replaced
# ${SENSOR_VAR} = SENSOR_PLACEHOLDER


# install packages
RUN apt-get update \
	&& apt-get upgrade -y \
	&& apt-get install -y --no-install-recommends \
	apt-utils \
	software-properties-common \
    nano \
    tmux \
    && mkdir -p /root/colcon_ws/src/${SENSOR_NODE}/src
    # -p no error if existing, make parent directories as needed

# copy binaries (mraa)
COPY usr/ /root/usr/.

# install python3.7 for mraa
RUN add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y python3.7 \
    && rm -rf /var/lib/apt/lists/* \
    # create necessary folders
    && mkdir /usr/lib/node_modules \
    && mkdir /usr/share/java \
    && mkdir /usr/lib/python3.7/dist-packages \
    && mkdir /usr/lib/python3.7/dist-packages/__pycache__ \
    && mkdir /usr/lib/python3.8/dist-packages/__pycache__ \
    # move binaries into right directory
    && mv /root/usr/bin/* /usr/bin/. \
    && mv /root/usr/share/java/* /usr/share/java/. \
    && mv /root/usr/include/mraa.h* /usr/include/. \
    && mv /root/usr/include/mraa /usr/include/. \
    && mv /root/usr/lib/aarch64-linux-gnu/libmraa* /usr/lib/aarch64-linux-gnu/. \
    && mv /root/usr/lib/aarch64-linux-gnu/pkgconfig/* /usr/lib/aarch64-linux-gnu/pkgconfig/. \
    && cp /root/usr/lib/python3.7/dist-packages/_mraa.so /usr/lib/python3.7/dist-packages. \
    && cp /root/usr/lib/python3.7/dist-packages/mraa.py /usr/lib/python3.7/dist-packages/. \
    && cp /root/usr/lib/python3.7/dist-packages/__pycache__/mraa.cpython-37.pyc /usr/lib/python3.7/dist-packages/__pycache__/. \
    && mv /root/usr/lib/python3.7/dist-packages/_mraa.so /usr/lib/python3.8/dist-packages/. \
    && mv /root/usr/lib/python3.7/dist-packages/mraa.py /usr/lib/python3.8/dist-packages/. \
    && mv /root/usr/lib/python3.7/dist-packages/__pycache__/mraa.cpython-37.pyc /usr/lib/python3.8/dist-packages/__pycache__/. \
    # libpython binaries needed for mraa
    && mv /root/usr/share/lintian/overrides/libpython3.7* /usr/share/lintian/overrides/. \
    && mv /root/usr/lib/aarch64-linux-gnu/libpython3.7m.so.1* /usr/lib/aarch64-linux-gnu/. \
    # test test test
    # trying to find the needed files for mraa spi SGP30 stuff...
    && mkdir /usr/lib/node_modules/mraa \
    && mv /root/usr/lib/mraa /usr/lib/node_modules/. \
    # libjson-c binaries needed for mraa
    && mv /root/usr/lib/aarch64-linux-gnu/libjson* /usr/lib/aarch64-linux-gnu/. \
    && rm -rf /root/usr \
    && cd /usr/lib/aarch64-linux-gnu/ \
    && ln -s libjson-c.so.3.0.1 libjson-c.so.3 \
    && rm libjsoncpp.so.1 \
    && ln -s libjsoncpp.so.1.7.4 libjsoncpp.so.1 \
    && ln -s libmraa.so.2 libmraa.so \
    && ln -s libmraa.so.2.2.0 libmraa.so.2 \
    && ln -s libpython3.7m.so.1.0 libpython3.7m.so.1

# Python updates needed for Blinka
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-wheel
RUN sudo pip3 install --upgrade setuptools
RUN pip3 install --upgrade pip


# Circuit Python Tool:
RUN pip3 install Adafruit-Blinka
# Sensor Library:
RUN sudo pip3 install adafruit-circuitpython-${SENSOR_VAR}


# ROS2 Dependencies
# for only Python should be used setup.py & .cfg but there are some issues with the --symlink-install option
#COPY CMakeLists.txt /root/colcon_ws/src/${SENSOR_NODE}/.
#COPY package.xml /root/colcon_ws/src/${SENSOR_NODE}/.
COPY README.md /root/colcon_ws/src/${SENSOR_NODE}/.
COPY src /root/colcon_ws/src/${SENSOR_NODE}/src/.
# Python Lib Folder (mandatory with init.py)
COPY ${SENSOR_NODE} /root/colcon_ws/src/${SENSOR_NODE}/${SENSOR_NODE}
# CPP Lib Folder not needed!
#COPY include /root/colcon_ws/src/${SENSOR_NODE}/include

# Make Python Files exectuable
RUN cd /root/colcon_ws/ \
    && chmod +x /root/colcon_ws/src/${SENSOR_NODE}/src/${SENSOR_VAR}.py

# Blinka walkaround
# Libs are located /usr/local/lib/python3.?/dist-packages
# python3.8 is the used in this image!
# complete folder from platformdetect and blinka has to be replaced as long as there is no offical release of the iot2050 or via git...!
COPY blinka/src /usr/local/lib/python3.8/dist-packages
COPY platformdetect /usr/local/lib/python3.8/dist-packages

#add sources to bashrc & build node
#RUN echo "source /opt/ros/galactic/setup.bash" >> ~/.bashrc \
#    && echo "source /root/colcon_ws/install/setup.bash" >> ~/.bashrc \
#    && cd /root/colcon_ws/ \
#    && . /opt/ros/galactic/setup.sh \
#	&& colcon build --symlink-install

# set workdirectory (my home directory)
WORKDIR /root/colcon_ws

# RUN Node
#CMD source /opt/ros/galactic/setup.bash \
#    && source install/setup.bash \
#    && ros2 run sgp30 sgp30_node
