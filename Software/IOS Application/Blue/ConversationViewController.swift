//
//  SecondViewController.swift
//  Blue
//
//  Created by 孙恩浩 on 27/01/2018.
//  Copyright © 2018 孙恩浩. All rights reserved.
//

import UIKit
import CoreBluetooth
import CoreMotion

extension String {
    //: ### Base64 encoding a string
    func base64Encoded() -> String? {
        if let data = self.data(using: .utf8) {
            return data.base64EncodedString()
        }
        return nil
    }
    
    //: ### Base64 decoding a string
    func base64Decoded() -> String? {
        if let data = Data(base64Encoded: self) {
            return String(data: data, encoding: .utf8)
        }
        return nil
    }
}
class ConversationViewController: UIViewController, UIPickerViewDelegate, UIPickerViewDataSource, CBPeripheralDelegate {

    @IBOutlet weak var windowStatus: UILabel!
    
    @IBOutlet weak var doorStatus: UILabel!
    @IBOutlet weak var lightStatus: UILabel!

    @IBOutlet weak var messageFromServer: UILabel!
    @IBOutlet weak var setPname: UILabel!
    @IBOutlet weak var acLabel: UILabel!

    @IBOutlet weak var replyButton: UIButton!
    @IBOutlet weak var load: UISwitch!
    @IBOutlet weak var subscribeServer: UISwitch!
    
    @IBOutlet weak var yesButton: UIButton!
    @IBOutlet weak var noButton: UIButton!
    @IBOutlet weak var disconnect: UIBarButtonItem!
    
    var peripheral: CBPeripheral!
    var centralManager: CBCentralManager!
    
    var writeCharacteristic: CBCharacteristic!
    var notifyCharacteristic: CBCharacteristic!
    let motionmanager = CMMotionManager()
    
    let timeInterval: TimeInterval = 0.2
    
    let uuid_write = "0001"
    let uuid_notify = "0002"
    var ax : Double = 1
    var ay : Double = 1
    var az : Double = 1
    var lastMessage : String!
    var decision : Bool = false
    var connected = false
    
    let windowstatus = ["OPEN", "CLOSED"]
    let doorstatus = ["OPEN", "SEMI_OPEN","CLOSED"]
    let lightstatus = ["ON", "OFF"]
    var editstatus : String!
    let editStatus = ["WINDOW", "DOOR", "LIGHT"]
    let alert = UIAlertController(title:"Status", message: "Choose status", preferredStyle: .actionSheet)
    
    let vc = UIViewController()
    let pickerView = UIPickerView(frame: CGRect(x: 0, y: 0, width: 150, height: 70))
    let editRadiusAlert = UIAlertController(title: "Choose status", message: "", preferredStyle: UIAlertControllerStyle.alert)
    func resetMessage(){
        lastMessage = nil
        messageFromServer.text = "no message received"
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        vc.preferredContentSize = CGSize(width: 150,height: 100)
        pickerView.delegate = self
        pickerView.dataSource = self
        vc.view.addSubview(pickerView)
        editRadiusAlert.setValue(vc, forKey: "contentViewController")
        editRadiusAlert.addAction(UIAlertAction(title: "Done", style: .default, handler: nil))

        setPname.text = peripheral.name
        //discovery callback
        peripheral.delegate = self
        
        //look for services
        peripheral.discoverServices(nil)
        
        // Do any additional setup after loading the view.

        messageFromServer.layer.cornerRadius = 10
        messageFromServer.layer.borderWidth = 0.7
        messageFromServer.layer.borderColor = UIColor.black.cgColor
        messageFromServer.layer.masksToBounds = true
        
        messageFromServer.lineBreakMode = NSLineBreakMode.byWordWrapping
        messageFromServer.numberOfLines = 0


        replyButton.setTitle("Reply", for: .normal)
        replyButton.setTitleColor(UIColor.white, for: .normal)
        
        yesButton.setTitleColor(UIColor.white, for: .normal)
        noButton.setTitleColor(UIColor.white, for: .normal)
        
        yesButton.backgroundColor = UIColor.green
        noButton.backgroundColor = UIColor.red
        
        replyButton.layer.cornerRadius = 10
        yesButton.layer.cornerRadius = 10
        noButton.layer.cornerRadius = 10
        
        disableReply()
        disableChoose()
        replyButton.addTarget(self, action: #selector(replyToServer), for: .touchUpInside)
        yesButton.addTarget(self, action: #selector(chooseYes), for: .touchUpInside)
        noButton.addTarget(self, action: #selector(chooseNo), for: .touchUpInside)
        disconnect.target = self
        disconnect.action = #selector(modifyConnection)

        let tapwindow = UITapGestureRecognizer(target: self, action: #selector(self.windowtapFun))
        windowStatus.isUserInteractionEnabled = true
        windowStatus.addGestureRecognizer(tapwindow)
        
        let tapdoor = UITapGestureRecognizer(target: self, action: #selector(self.doortapFunc))
        doorStatus.isUserInteractionEnabled = true
        doorStatus.addGestureRecognizer(tapdoor)
        
        let taplight = UITapGestureRecognizer(target: self, action: #selector(self.lighttapFunc))
        lightStatus.isUserInteractionEnabled = true
        lightStatus.addGestureRecognizer(taplight)
        
        load.addTarget(self, action: #selector(switchDidChange), for: UIControlEvents.valueChanged)
        self.subscribeServer.addTarget(self, action: #selector(subscribe), for: UIControlEvents.valueChanged)
        startAccelerometerUpdates()
    }
    
    @objc func windowtapFun(sender: UITapGestureRecognizer){
        editstatus = editStatus[0]
        self.pickerView.reloadAllComponents()
        self.present(editRadiusAlert, animated: true)
    }
    
    @objc func doortapFunc(sender: UITapGestureRecognizer){
        editstatus = editStatus[1]
        self.pickerView.reloadAllComponents()
        self.present(editRadiusAlert, animated: true)
    }
    @objc func lighttapFunc(sender: UITapGestureRecognizer){
        editstatus = editStatus[2]
        self.pickerView.reloadAllComponents()
        self.present(editRadiusAlert, animated: true)
    }
    @objc func numberOfpeopletapFunc(sender: UITapGestureRecognizer){
        editstatus = editStatus[3]
        self.pickerView.reloadAllComponents()
        self.present(editRadiusAlert, animated: true)
    }
   
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        if editstatus == "WINDOW"{
            return windowstatus[row]
        }else if editstatus == "DOOR"{
            return doorstatus[row]
        }else if editstatus == "LIGHT"{
            return lightstatus[row]
        }else{
            return "NONE"
        }
    }
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        if editstatus == "WINDOW"{
            return windowstatus.count
        }else if editstatus == "DOOR"{
            return doorstatus.count
        }else if editstatus == "LIGHT"{
            return lightstatus.count
        }else{
            return 1
        }
    }
    func pickerView(_ pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
        if editstatus == "WINDOW"{
            windowStatus.text = windowstatus[row]
        }else if editstatus == "DOOR"{
            doorStatus.text = doorstatus[row]
        }else if editstatus == "LIGHT"{
            lightStatus.text = lightstatus[row]
        }else{
            //do nothing
        }
    }
    
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    //UISwitch
    @objc func switchDidChange(){
       
    }
    
    @objc func modifyConnection() {
        if(connected == true){
            print("ready to dis")
            centralManager?.cancelPeripheralConnection(peripheral)
            connected = false
            disconnect.title = ""
            disableAllButton()
        }
    }
    
    func disableAllButton(){
        disableReply()
        disableChoose()
        load.isOn = false
        load.isHidden = true
        subscribeServer.isOn = false
        subscribeServer.isHidden = true
        disconnect.isEnabled = false
    }

    @objc func subscribe(){
        if subscribeServer.isOn{
            if notifyCharacteristic != nil{
                peripheral.setNotifyValue(true, for: notifyCharacteristic)
            }else{
                subscribeServer.setOn(false, animated: true)
            }
        }else{
            if(notifyCharacteristic != nil){
                peripheral.setNotifyValue(false, for: notifyCharacteristic)
            }else{
                subscribeServer.setOn(true, animated: true)
            }
        }
    }
    func disableChoose(){
        yesButton.isEnabled = false
        noButton.isEnabled = false
        yesButton.backgroundColor = UIColor.gray
        noButton.backgroundColor = UIColor.gray
    }
    func enableChoose(){
        yesButton.isEnabled = true
        noButton.isEnabled = true
        yesButton.backgroundColor = UIColor.green
        noButton.backgroundColor = UIColor.red
    }
    func disableReply(){
        replyButton.isEnabled = false
        replyButton.backgroundColor = UIColor.gray
    }
    func enableReply(){
        replyButton.isEnabled = true
        replyButton.backgroundColor = UIColor.black
    }
    //reply button action
    @objc func replyToServer(){
        let firstindex = lastMessage.index(of: "(") ?? lastMessage.endIndex
        let lastindex = lastMessage.index(of: "\n") ?? lastMessage.endIndex
        var message = String(lastMessage[firstindex..<lastindex])
        if(decision){
            message += "1"
            self.writeToPeripheral(message: message)
        }else{
            message += "0"
            self.writeToPeripheral(message: message)
        }
        lastMessage = nil
        messageFromServer.text = "no message from server"
        disableReply()
        disableChoose()
    }
    
    @objc func chooseYes(){
        print("enable reply")
        decision = true
        yesButton.backgroundColor = UIColor.green
        noButton.backgroundColor = UIColor.gray
        enableReply()
    }
    
    @objc func chooseNo(){
        decision = false
        noButton.backgroundColor = UIColor.red
        yesButton.backgroundColor = UIColor.gray
        enableReply()
    }

    func startAccelerometerUpdates(){
        motionmanager.deviceMotionUpdateInterval = 1/10
        let queue = OperationQueue.current
        motionmanager.startDeviceMotionUpdates(to: queue!, withHandler: {
            (deviceMotion, error) in
            var text = "--accelerometer--\n"
            let acceleration = deviceMotion!.userAcceleration
            self.ax = acceleration.x
            self.ay = acceleration.y
            self.az = acceleration.z
            text += "ux: \(self.ax)\n"
            text += "uy: \(self.ay)\n"
            text += "uz: \(self.az)\n"
            if self.load.isOn {
                var text = "x\(String(format: "%.5f", self.ax))"
                text += "y\(String(format: "%.5f", self.ay))"
                text += "z\(String(format: "%.5f", self.az))"
                self.writeToPeripheral(message: text)
            }
        })
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

     // discoverd peripheral service
     func peripheral(_ peripheral: CBPeripheral, didDiscoverServices error: Error?) {
        guard let services = peripheral.services else{ return }
        for service in services{
            print(service)
            peripheral.discoverCharacteristics(nil, for: service)
        }
     }
     
     // discover peripheral characteristic
     func peripheral(_ peripheral: CBPeripheral, didDiscoverCharacteristicsFor service: CBService, error: Error?) {
        guard let characteristics = service.characteristics else { return }
        for characteristic in characteristics{
            if characteristic.properties.contains(CBCharacteristicProperties.write){
                if characteristic.uuid.uuidString == uuid_write{
                    writeCharacteristic = characteristic
                }
            }
            if characteristic.properties.contains(CBCharacteristicProperties.notify){
                if characteristic.uuid.uuidString == uuid_notify{
                    notifyCharacteristic = characteristic
                }
            }
        }
     }
     
    func writeToPeripheral(message:String){
        if writeCharacteristic != nil{
            let messageData = message.data(using: String.Encoding.utf8)
            self.peripheral.writeValue(messageData!, for: writeCharacteristic, type: CBCharacteristicWriteType.withResponse)
        }else{
        }
     }
    
     // write value to peripheral
     func peripheral(_ peripheral: CBPeripheral, didWriteValueFor characteristic: CBCharacteristic, error: Error?) {
        print("didWriteValueForCharacteristic")
     }
    
    func peripheral(_ peripheral: CBPeripheral, didUpdateNotificationStateFor characteristic: CBCharacteristic, error: Error?) {
        print("-----didUpdateNotificationStateForCharacteristic-----")
        if (error != nil) {
            print("Error");
        }
        //Notification has started
        if characteristic.isNotifying {
            print("start notify\(characteristic)")
            peripheral.readValue(for: characteristic)
        }
    }
     // update
     func peripheral(_ peripheral: CBPeripheral, didUpdateValueFor characteristic: CBCharacteristic, error: Error?) {
        print("DidUpdateValue for characteristics")
        
        if(characteristic.value?.base64EncodedString() == nil){
            print("no message received")
            lastMessage = "no message received"
            messageFromServer.text = lastMessage
        }else{
            let str = characteristic.value?.base64EncodedString()
            let t = str?.base64Decoded()
            if(t == "0"){
                lastMessage = "no message received"
                messageFromServer.text = lastMessage
                print("t is nil")
            }else{
                lastMessage = t!
                messageFromServer.text = lastMessage
                enableChoose()
            }
        }
     }
    
}
