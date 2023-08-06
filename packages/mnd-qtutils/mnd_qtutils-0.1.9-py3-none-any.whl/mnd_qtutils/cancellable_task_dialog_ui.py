<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>273</width>
    <height>93</height>
   </rect>
  </property>
  <property name="sizePolicy">
   <sizepolicy hsizetype="Preferred" vsizetype="Preferred">
    <horstretch>0</horstretch>
    <verstretch>0</verstretch>
   </sizepolicy>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <layout class="QVBoxLayout" name="verticalLayout">
   <property name="leftMargin">
    <number>0</number>
   </property>
   <property name="topMargin">
    <number>0</number>
   </property>
   <property name="rightMargin">
    <number>0</number>
   </property>
   <property name="bottomMargin">
    <number>0</number>
   </property>
   <item>
    <widget class="QWidget" name="info_layout" native="true">
     <layout class="QHBoxLayout" name="horizontalLayout">
      <item>
       <widget class="QLabel" name="info_label">
        <property name="text">
         <string/>
        </property>
       </widget>
      </item>
      <item>
       <widget class="QLabel" name="percent_label">
        <property name="text">
         <string/>
        </property>
        <property name="alignment">
         <set>Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter</set>
        </property>
       </widget>
      </item>
     </layout>
    </widget>
   </item>
   <item>
    <widget class="QWidget" name="button_widget" native="true">
     <layout class="QHBoxLayout" name="horizontalLayout_2">
      <property name="leftMargin">
       <number>0</number>
      </property>
      <property name="topMargin">
       <number>0</number>
      </property>
      <property name="rightMargin">
       <number>0</number>
      </property>
      <property name="bottomMargin">
       <number>0</number>
      </property>
      <item>
       <spacer name="horizontalSpacer">
        <property name="orientation">
         <enum>Qt::Horizontal</enum>
        </property>
        <property name="sizeHint" stdset="0">
         <size>
          <width>40</width>
          <height>20</height>
         </size>
        </property>
       </spacer>
      </item>
      <item>
       <widget class="QPushButton" name="cancel_button">
        <property name="text">
         <string>Cancelar</string>
        </property>
       </widget>
      </item>
     </layout>
    </widget>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections/>
</ui>
