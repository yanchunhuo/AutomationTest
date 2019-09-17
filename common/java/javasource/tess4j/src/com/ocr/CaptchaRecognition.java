package com.ocr;

import java.io.File;

import org.apache.xmlgraphics.util.io.Base64DecodeStream;

import net.sourceforge.tess4j.ITesseract;
import net.sourceforge.tess4j.Tesseract;
import net.sourceforge.tess4j.TesseractException;

public class CaptchaRecognition {
	private String tessdata_dir;
	private ITesseract instance;
	
	public static void main(String[] args) {
		CaptchaRecognition captchaRecognition=new CaptchaRecognition("libs/tessdata");
		//String result=captchaRecognition.captchaRecognitionWithFile("E:\\gitserver\\code\\jiweitech\\WEBUIAutomationTest\\output\\firefox\\20181214124719379000_captcha.png", "eng");
		String result=captchaRecognition.captchaRecognitionWithFile("image/20181214134519224000_captcha.png", "eng");
		System.out.println(result);
	}
	
	public CaptchaRecognition(String tessdata_dir){
		this.tessdata_dir=tessdata_dir;
		this.instance=new Tesseract();
		this.instance.setDatapath(this.tessdata_dir);
	}
	
	/**
	 * 
	 * @param imageFilePath
	 * @param language eng:英文，chi_sim:中文
	 * @return
	 */
	public String captchaRecognitionWithFile(String imageFilePath,String language){
		this.instance.setLanguage(language);
		File imageFile=new File(imageFilePath);
		String result = null;
		try {
			result = this.instance.doOCR(imageFile);
		} catch (TesseractException e) {
			e.printStackTrace();
		}
		return result;
	}
}
