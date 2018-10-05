using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Linq.Expressions;
using System.Security.Cryptography;
using System.Text;
using System.Web;
using System.Web.Mvc;
using System.Web.Mvc.Html;

namespace ASP.NET_MVC_Application.Extensions
{
    public static class CustomEnumDropdownList
    {
        public static MvcHtmlString CustomEnumDropDownListFor<TModel, TEnum>(
  this HtmlHelper<TModel> htmlHelper, Expression<Func<TModel, TEnum>> expression, object htmlAttributes)
        {
            var metadata = ModelMetadata.FromLambdaExpression(expression, htmlHelper.ViewData);
            var values = Enum.GetValues(typeof(TEnum)).Cast<TEnum>();

            var items =
                values.Select(
                   value =>
                   new SelectListItem
                   {
                       Text = GetEnumDescription(value),
                       Value = value.ToString(),
                       Selected = value.Equals(metadata.Model)
                   });
            var attributes = HtmlHelper.AnonymousObjectToHtmlAttributes(htmlAttributes);
            return htmlHelper.DropDownListFor(expression, items, attributes);
        }

        public static string GetEnumDescription<TEnum>(this TEnum value)
        {
            var field = value.GetType().GetField(value.ToString());
            var attributes = (DescriptionAttribute[])field.GetCustomAttributes(typeof(DescriptionAttribute), false);
            return attributes.Length > 0 ? attributes[0].Description : value.ToString();
        }
    }


    public static class CryptographyExtensions
{
	/// <summary>
	/// 	Calculates the MD5 hash for the given string.
	/// </summary>
	/// <returns>A 32 char long MD5 hash.</returns>
	public static string GetHashMd5(this string input)
	{
		return ComputeHash(input, new MD5CryptoServiceProvider());
	}

	/// <summary>
	/// 	Calculates the SHA-1 hash for the given string.
	/// </summary>
	/// <returns>A 40 char long SHA-1 hash.</returns>
	public static string GetHashSha1(this string input)
	{
		return ComputeHash(input, new SHA1Managed());
	}

	/// <summary>
	/// 	Calculates the SHA-256 hash for the given string.
	/// </summary>
	/// <returns>A 64 char long SHA-256 hash.</returns>
	public static string GetHashSha256(this string input)
	{
		return ComputeHash(input, new SHA256Managed());
	}

	/// <summary>
	/// 	Calculates the SHA-384 hash for the given string.
	/// </summary>
	/// <returns>A 96 char long SHA-384 hash.</returns>
	public static string GetHashSha384(this string input)
	{
		return ComputeHash(input, new SHA384Managed());
	}

	/// <summary>
	/// 	Calculates the SHA-512 hash for the given string.
	/// </summary>
	/// <returns>A 128 char long SHA-512 hash.</returns>
	public static string GetHashSha512(this string input)
	{
		return ComputeHash(input, new SHA512Managed());
	}

	public static string ComputeHash(string input, HashAlgorithm hashProvider)
	{
		if (input == null)
		{
			throw new ArgumentNullException("input");
		}

		if (hashProvider == null)
		{
			throw new ArgumentNullException("hashProvider");
		}

		var inputBytes = Encoding.UTF8.GetBytes(input);
		var hashBytes = hashProvider.ComputeHash(inputBytes);
		var hash = BitConverter.ToString(hashBytes).Replace("-", string.Empty);

		return hash;
	}
}
}